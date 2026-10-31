#!/usr/bin/env python3
"""Convert BTL riel.md body into structured LaTeX chapter files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/home/nhanlx05/projects/bao-cao-pttk-ptit")
MD = ROOT / "BTL riel.md"

IMAGE_CAPTIONS = {
    "image1": ("Thư viện ReactJS dùng cho giao diện người dùng", "fig:reactjs"),
    "image2": ("Ngôn ngữ lập trình Java dùng cho backend", "fig:java"),
    "image3": ("Hệ quản trị cơ sở dữ liệu PostgreSQL", "fig:postgresql"),
    "image4": ("Sơ đồ lớp phân tích UC03 -- Sinh viên gửi yêu cầu đặt phòng", "fig:uc03-class"),
}

PLACEHOLDER_HEADINGS = {
    "tác nhân, tiền điều kiện và hậu điều kiện",
    "luồng sự kiện chính",
    "luồng thay thế và ngoại lệ",
    "quy tắc nghiệp vụ và dữ liệu liên quan",
    "sơ đồ lớp uc01",
    "sơ đồ lớp uc02",
    "sơ đồ lớp uc05",
    "sơ đồ lớp uc06",
    "sơ đồ lớp uc07",
    "sơ đồ lớp uc08",
    "quan hệ nghiệp vụ giữa uc01 và uc02",
    "biểu đồ use case tổng quát",
    "biểu đồ use case phân rã theo chức năng",
    "mục đích và mô tả chức năng",
    "biểu đồ hoạt động uc10",
    "dữ liệu liên quan",
}


def strip_md_markup(s: str) -> str:
    s = s.strip()
    s = s.replace("**", "")
    s = s.strip("# ").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def latex_escape(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    repl = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    s = s.replace(" = ", " = ")
    s = s.replace(r"\=", "=")
    return s


def inline(s: str) -> str:
    s = s.replace("\\=", "=")
    s = s.strip()
    # protect bold/italic first via placeholders
    parts: list[str] = []
    i = 0
    while i < len(s):
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j != -1:
                parts.append("\\textbf{" + latex_escape(s[i + 2 : j]) + "}")
                i = j + 2
                continue
        if s[i] == "*" and (i + 1 < len(s) and s[i + 1] != " "):
            j = s.find("*", i + 1)
            if j != -1 and j > i + 1:
                parts.append("\\textit{" + latex_escape(s[i + 1 : j]) + "}")
                i = j + 1
                continue
        if s.startswith("``", i):
            j = s.find("``", i + 2)
            if j != -1:
                parts.append("\\texttt{" + latex_escape(s[i + 2 : j]) + "}")
                i = j + 2
                continue
        if s[i] == "`":
            j = s.find("`", i + 1)
            if j != -1:
                parts.append("\\texttt{" + latex_escape(s[i + 1 : j]) + "}")
                i = j + 1
                continue
        # consume until next special
        nxt = len(s)
        for token in ("**", "`"):
            p = s.find(token, i + 1)
            if p != -1:
                nxt = min(nxt, p)
        pstar = s.find("*", i + 1)
        if pstar != -1:
            nxt = min(nxt, pstar)
        parts.append(latex_escape(s[i:nxt]))
        i = nxt
    return "".join(parts)


def is_table_line(line: str) -> bool:
    t = line.strip()
    return t.startswith("|") and t.endswith("|")


def is_table_sep(line: str) -> bool:
    t = line.replace(" ", "")
    return bool(re.match(r"^\|?(:?-+:?\|)+$", t))


def parse_row(line: str) -> list[str]:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def table_to_latex(rows: list[list[str]], caption: str | None, label: str | None) -> str:
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    header, body = rows[0], rows[1:]
    colspec = "|>{\\raggedright\\arraybackslash}p{0.22\\textwidth}" + "|>{\\raggedright\\arraybackslash}p{0.22\\textwidth}" * (ncol - 2) + "|>{\\raggedright\\arraybackslash}X|"
    if ncol == 2:
        colspec = "|>{\\raggedright\\arraybackslash}p{0.32\\textwidth}|>{\\raggedright\\arraybackslash}X|"
    if ncol == 3:
        colspec = "|>{\\raggedright\\arraybackslash}p{0.28\\textwidth}|>{\\raggedright\\arraybackslash}X|>{\\raggedright\\arraybackslash}p{0.28\\textwidth}|"
    if ncol == 4:
        colspec = "|>{\\raggedright\\arraybackslash}p{0.18\\textwidth}|>{\\raggedright\\arraybackslash}X|>{\\raggedright\\arraybackslash}p{0.22\\textwidth}|>{\\raggedright\\arraybackslash}p{0.18\\textwidth}|"
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\small",
    ]
    if caption:
        cap = caption.strip().strip("*").strip().replace("\\.", ".")
        cap = re.sub(r"^Bảng\s+[\d.]+\s*", "", cap)
        lines.append(r"\caption{" + inline(cap) + "}")
    elif label:
        lines.append(r"\caption{Bảng dữ liệu đặc tả}")
    if label:
        lines.append(r"\label{" + label + "}")
    lines.extend(
        [
            r"\begin{tabularx}{\textwidth}{" + colspec + "}",
            r"\hline",
            " & ".join(f"\\textbf{{{inline(c)}}}" for c in header) + r" \\",
            r"\hline",
        ]
    )
    for r in body:
        lines.append(" & ".join(inline(c) for c in r) + r" \\")
        lines.append(r"\hline")
    lines.append(r"\end{tabularx}")
    lines.append(r"\end{table}")
    lines.append("")
    return "\n".join(lines)


def figure_to_latex(key: str, caption_line: str | None) -> str:
    cap, lab = IMAGE_CAPTIONS.get(key, (f"Hình minh họa {key}", f"fig:{key}"))
    if caption_line:
        c = caption_line.strip().strip("*").strip().replace("\\.", ".")
        c = re.sub(r"^Hình\s+[\d.]+\s*", "", c).strip(" .")
        if c:
            cap = c
    return "\n".join(
        [
            r"\begin{figure}[H]",
            r"\centering",
            rf"\includegraphics[width=0.72\textwidth]{{assets/{key}.png}}",
            rf"\caption{{{cap}}}",
            rf"\label{{{lab}}}",
            r"\end{figure}",
            "",
        ]
    )


def _title_from_rest(rest: str) -> tuple[int | None, str]:
    """Return (dot-count of numbering, display title)."""
    title = strip_md_markup(rest)
    title = title.replace("\\.", ".")
    num = re.match(r"^(\d+(?:\.\d+)*)\s+(.*)$", title)
    dots = None
    if num:
        dots = num.group(1).count(".")
        title = num.group(2)
    title = re.sub(r"^[a-f]\.\s*", "", title, flags=re.I)
    title = re.sub(r"^[a-f]\.(?=[A-ZÀÁẢÃẠĂÂÊÔƠƯĐ])", "", title, flags=re.I)
    return dots, title.strip()


def heading_level_and_title(line: str) -> tuple[int, str] | None:
    raw = line.strip()
    if not raw or raw in ("**LỜI MỞ ĐẦU**", "**MỤC LỤC**"):
        return None
    m = re.match(r"^(#{1,6})\s+(.*)$", raw)
    if m:
        hashes, rest = m.group(1), m.group(2)
        dots, title = _title_from_rest(rest)
        if dots is not None:
            # 2.1 -> section, 2.1.1 -> subsection, 2.4.1.1 -> subsubsection
            lvl = min(dots, 3)
        else:
            lvl = len(hashes)
        return lvl, title
    m = re.match(r"^\d+\.\s+(#{1,6})\s+(.*)$", raw)
    if m:
        dots, title = _title_from_rest(m.group(2))
        lvl = 1 if len(m.group(1)) == 1 else 2
        return lvl, title
    return None


CHAPTER_TITLES = {
    "CHƯƠNG I: GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ": "GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ",
    "CHƯƠNG II: PHÂN TÍCH HỆ THỐNG": "PHÂN TÍCH HỆ THỐNG",
}


def normalize_title(title: str) -> str:
    title = title.replace("dề tài", "đề tài")
    title = title.replace("UseCase", "Use Case")
    title = title.replace("ReactJs", "ReactJS")
    title = title.replace("PosgreSql", "PostgreSQL")
    upper = title.upper()
    if upper.startswith("CHƯƠNG II"):
        return "PHÂN TÍCH HỆ THỐNG"
    if re.match(r"^CHƯƠNG I\b", upper) and "GIỚI THIỆU" in upper:
        return "GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ"
    # drop leftover "2.4.1.1 " already stripped
    return title


def is_paragraph_heading(title: str) -> bool:
    t = title.lower()
    keys = (
        "giai đoạn",
        "luồng thay thế",
        "luồng ngoại lệ",
        "quy tắc nghiệp vụ",
        "dữ liệu liên quan",
        "mục đích",
        "mô tả",
        "phòng, giường",
        "đặt phòng:",
        "hợp đồng, bàn giao",
        "khoản phí:",
        "trả phòng:",
        "xử lý đồng thời",
    )
    return t.startswith(keys) or t.rstrip(":") in {
        "phòng, giường",
        "đặt phòng",
        "hợp đồng, bàn giao",
        "khoản phí",
        "trả phòng",
        "xử lý đồng thời",
        "luồng thay thế",
        "luồng ngoại lệ",
        "quy tắc nghiệp vụ",
        "dữ liệu liên quan",
    }


def convert_body(lines: list[str]) -> dict[str, list[str]]:
    files = {
        "ch1": [r"\clearpage", r"\chapter{GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ}", ""],
        "ch2": [r"\clearpage", r"\chapter{PHÂN TÍCH HỆ THỐNG}", ""],
    }
    current = "ch1"
    i = 0
    n = len(lines)
    table_counter = {"ch1": 0, "ch2": 0}
    last_heading_empty = False
    last_heading_title = ""

    def out() -> list[str]:
        return files[current]

    def mark_content():
        nonlocal last_heading_empty
        last_heading_empty = False

    while i < n:
        line = lines[i]
        raw = line.rstrip()
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue
        if stripped in ("**LỜI MỞ ĐẦU**", "**MỤC LỤC**"):
            i += 1
            continue

        # chapter switch
        ht = heading_level_and_title(stripped)
        if ht:
            lvl, title = ht
            title = normalize_title(title)
            if title in CHAPTER_TITLES.values() or title.upper().startswith("CHƯƠNG"):
                if title == "PHÂN TÍCH HỆ THỐNG":
                    current = "ch2"
                elif title == "GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ":
                    current = "ch1"
                i += 1
                continue
            # skip empty leftover headings
            if not title:
                i += 1
                continue

            # flush placeholder if previous heading had no content
            if last_heading_empty and last_heading_title:
                key = last_heading_title.lower()
                if any(p in key for p in PLACEHOLDER_HEADINGS) or True:
                    # only add placeholder when next is also heading (we'll check after)
                    pass

            cmd = {1: r"\section", 2: r"\subsection", 3: r"\subsubsection", 4: r"\paragraph"}.get(
                lvl, r"\subsubsection"
            )
            if current == "ch1":
                ch1_sections = {
                    "Giới thiệu đề tài",
                    "Đối tượng sử dụng và phạm vi hệ thống",
                    "Quy trình nghiệp vụ tổng quát",
                    "Định hướng giải pháp công nghệ",
                }
                cmd = r"\section" if title in ch1_sections else r"\subsection"

            # lettered items like a. b. already stripped; if original was ### it's subsubsection
            out().append(f"{cmd}{{{latex_escape(title)}}}")
            out().append("")
            last_heading_empty = True
            last_heading_title = title
            i += 1
            continue

        # bold-only pseudo headings
        if stripped.startswith("**") and stripped.endswith("**") and stripped.count("**") == 2 and len(stripped) < 120:
            title = normalize_title(strip_md_markup(stripped))
            if title:
                out().append(r"\paragraph{" + latex_escape(title) + "}")
                out().append("")
                last_heading_empty = True
                last_heading_title = title
                i += 1
                continue

        # figure
        fm = re.match(r"!\[(.*?)\]\[(image\d+)\]", stripped)
        if fm:
            cap = None
            if i + 2 < n and lines[i + 1].strip() == "" and lines[i + 2].strip().startswith("*Hình"):
                cap = lines[i + 2].strip()
                i += 3
            elif i + 1 < n and lines[i + 1].strip().startswith("*Hình"):
                cap = lines[i + 1].strip()
                i += 2
            else:
                i += 1
            out().append(figure_to_latex(fm.group(2), cap))
            mark_content()
            continue

        # table
        if is_table_line(stripped):
            rows: list[list[str]] = []
            while i < n and is_table_line(lines[i].strip()):
                if not is_table_sep(lines[i].strip()):
                    rows.append(parse_row(lines[i]))
                i += 1
            cap = None
            # skip blanks then caption
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and (lines[j].strip().startswith("*Bảng") or lines[j].strip().startswith("*Bảng")):
                cap = lines[j].strip()
                i = j + 1
            table_counter[current] += 1
            lab = f"tab:{current}-{table_counter[current]}"
            out().append(table_to_latex(rows, cap, lab))
            mark_content()
            continue

        # numbered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n:
                s = lines[i].strip()
                if not s:
                    # peek
                    i += 1
                    if i < n and (re.match(r"^\d+\.\s+", lines[i].strip()) or lines[i].strip().startswith("*")):
                        continue
                    break
                mnum = re.match(r"^(\d+)\.\s+(.*)$", s)
                if mnum:
                    items.append(("num", mnum.group(2)))
                    i += 1
                    # nested bullets immediately after
                    while i < n and (lines[i].startswith("   *") or lines[i].startswith("  *") or re.match(r"^\s+\*\s+", lines[i])):
                        items.append(("sub", lines[i].strip()[1:].strip()))
                        i += 1
                    continue
                break
            out().append(r"\begin{enumerate}[leftmargin=1.6em]")
            k = 0
            while k < len(items):
                kind, text = items[k]
                if kind == "num":
                    subs = []
                    k += 1
                    while k < len(items) and items[k][0] == "sub":
                        subs.append(items[k][1])
                        k += 1
                    if subs:
                        out().append(r"\item " + inline(text))
                        out().append(r"\begin{itemize}")
                        for sub in subs:
                            out().append(r"\item " + inline(sub))
                        out().append(r"\end{itemize}")
                    else:
                        out().append(r"\item " + inline(text))
                else:
                    k += 1
            out().append(r"\end{enumerate}")
            out().append("")
            mark_content()
            continue

        # bullet list (including - )
        if stripped.startswith("* ") or stripped.startswith("- ") or stripped.startswith("*"):
            if stripped in ("*", "-", "* "):
                i += 1
                continue
            out().append(r"\begin{itemize}[leftmargin=1.4em]")
            while i < n:
                s = lines[i].strip()
                if not s:
                    i += 1
                    if i < n and (lines[i].strip().startswith("*") or lines[i].strip().startswith("- ")):
                        continue
                    break
                if s.startswith("*") or s.startswith("- "):
                    text = s.lstrip("*- ").strip()
                    if text:
                        out().append(r"\item " + inline(text))
                    i += 1
                    continue
                break
            out().append(r"\end{itemize}")
            out().append("")
            mark_content()
            continue

        # caption-only leftover
        if stripped.startswith("*Bảng") or stripped.startswith("*Hình"):
            i += 1
            continue

        # normal paragraph: gather wrapped lines until blank
        para = [stripped]
        i += 1
        while i < n:
            nxt = lines[i].rstrip()
            ns = nxt.strip()
            if not ns:
                break
            if heading_level_and_title(ns) or is_table_line(ns) or ns.startswith("![") or re.match(r"^\d+\.\s+", ns) or ns.startswith("* ") or ns.startswith("- "):
                break
            if ns.startswith("**") and ns.endswith("**") and ns.count("**") == 2 and len(ns) < 120:
                break
            para.append(ns)
            i += 1
        text = " ".join(para)
        # skip process arrows as itemize-like emphasize
        if "→" in text and text.startswith("**") is False:
            out().append(r"\begin{center}")
            out().append(r"\textbf{" + latex_escape(re.sub(r"\*+", "", text)) + "}")
            out().append(r"\end{center}")
            out().append("")
        else:
            out().append(inline(text))
            out().append("")
        mark_content()

    return files


def add_placeholders(tex_lines: list[str]) -> list[str]:
    """If a structural heading is followed immediately by another heading, insert a note."""
    heading_cmds = (r"\section{", r"\subsection{", r"\subsubsection{")
    out: list[str] = []
    i = 0
    while i < len(tex_lines):
        line = tex_lines[i]
        out.append(line)
        if any(line.startswith(cmd) for cmd in heading_cmds):
            j = i + 1
            while j < len(tex_lines) and tex_lines[j].strip() == "":
                j += 1
            nxt = tex_lines[j] if j < len(tex_lines) else ""
            if j >= len(tex_lines) or any(nxt.startswith(cmd) for cmd in heading_cmds):
                title = line.lower()
                interesting = ("sơ đồ", "biểu đồ", "luồng", "quy tắc", "tác nhân", "mục đích", "quan hệ nghiệp vụ")
                if any(k in title for k in interesting):
                    out.append(r"\textit{Phần này đang được bổ sung trong các phiên bản tiếp theo của báo cáo.}")
                    out.append("")
        i += 1
    return out


INTRO = r"""
\clearpage
\chapter*{MỞ ĐẦU}
\phantomsection
\addcontentsline{toc}{chapter}{MỞ ĐẦU}

\section*{1. Lý do chọn đề tài}
\phantomsection
\addcontentsline{toc}{section}{1. Lý do chọn đề tài}

Ký túc xá là bộ phận hỗ trợ trực tiếp đời sống học tập của sinh viên. Trong quá trình vận hành, cán bộ phải theo dõi số lượng phòng và giường, tiếp nhận nhu cầu ở nội trú, bố trí chỗ ở, lập hợp đồng, ghi nhận các khoản phí và xử lý việc trả phòng. Những nghiệp vụ này liên kết chặt chẽ với nhau vì một thay đổi ở trạng thái giường có thể ảnh hưởng đến kết quả tìm phòng, yêu cầu đặt phòng, hợp đồng và khả năng tiếp nhận sinh viên mới.

Khi dữ liệu được ghi chép ở nhiều sổ hoặc tệp riêng lẻ, cán bộ khó xác định trạng thái phòng tại cùng một thời điểm. Sinh viên cũng cần một kênh thống nhất để tìm phòng phù hợp, gửi yêu cầu đặt phòng, theo dõi khoản phí và đề nghị trả phòng. Vì vậy, đề tài \textbf{Hệ thống quản lý ký túc xá PTIT} được lựa chọn nhằm xây dựng một quy trình xuyên suốt, trong đó dữ liệu của giai đoạn trước trở thành cơ sở cho giai đoạn sau nhưng mỗi chức năng vẫn có ranh giới xử lý riêng.

Đề tài phù hợp với nội dung học phần Phân tích và thiết kế hệ thống thông tin vì chứa nhiều đối tượng nghiệp vụ có quan hệ rõ ràng và các quy tắc cần kiểm soát, chẳng hạn không giữ một giường cho nhiều sinh viên trong cùng thời gian, không lập hai hợp đồng còn hiệu lực cho một sinh viên và không giải phóng giường trước khi hoàn tất trả phòng.

\section*{2. Mục tiêu đề tài}
\phantomsection
\addcontentsline{toc}{section}{2. Mục tiêu đề tài}

Mục tiêu tổng quát là xây dựng mô hình hệ thống thông tin hỗ trợ quản lý vòng đời chỗ ở của sinh viên tại ký túc xá, tạo nguồn dữ liệu thống nhất để sinh viên và cán bộ sử dụng theo đúng quyền hạn.

Các mục tiêu cụ thể gồm:
\begin{itemize}[leftmargin=1.4em]
\item Cung cấp thông tin phòng và giường còn khả dụng để sinh viên tìm kiếm theo nhu cầu thực tế.
\item Ghi nhận yêu cầu đặt phòng và hỗ trợ cán bộ giữ một chỗ cụ thể cho sinh viên.
\item Hỗ trợ lập hợp đồng và xác nhận bàn giao phòng theo các điều kiện đã xác định.
\item Theo dõi khoản phí nội trú và ghi nhận kết quả thanh toán của sinh viên.
\item Tiếp nhận yêu cầu trả phòng, kết thúc hợp đồng và giải phóng giường theo đúng quy trình.
\item Tạo cơ sở dữ liệu đủ nhất quán để phục vụ tra cứu, kiểm tra và mở rộng báo cáo sau này.
\end{itemize}

\section*{3. Đối tượng nghiên cứu}
\phantomsection
\addcontentsline{toc}{section}{3. Đối tượng nghiên cứu}

Đối tượng nghiên cứu là quy trình quản lý chỗ ở tại ký túc xá, gồm hai tác nhân chính: sinh viên và cán bộ quản lý ký túc xá. Các đối tượng dữ liệu được khảo sát gồm phòng, giường, yêu cầu đặt phòng, giữ chỗ, hợp đồng, bàn giao, khoản phí, giao dịch thanh toán và yêu cầu trả phòng.

\section*{4. Phạm vi nghiên cứu}
\phantomsection
\addcontentsline{toc}{section}{4. Phạm vi nghiên cứu}

Phạm vi chức năng gồm mười Use Case, tổ chức theo năm giai đoạn của vòng đời chỗ ở: xem phòng (UC01, UC02), đặt phòng (UC03, UC04), thuê phòng (UC05, UC06), đóng phí (UC07, UC08) và trả phòng (UC09, UC10).

Đề tài chưa xử lý các nghiệp vụ không trực tiếp thuộc vòng đời chỗ ở như quản lý khách ra vào, đăng ký tạm trú, quản lý bưu phẩm, sửa chữa cơ sở vật chất, xử lý vi phạm nội trú và thống kê điện nước chi tiết. Tích hợp cổng thanh toán thực tế, ký số hợp đồng và đồng bộ với hệ thống đào tạo được xem là hướng mở rộng.

\section*{5. Phương pháp nghiên cứu}
\phantomsection
\addcontentsline{toc}{section}{5. Phương pháp nghiên cứu}

Nhóm vận dụng phương pháp phân tích và thiết kế hướng đối tượng, mô hình hóa bằng UML. Phần phân tích xác định tác nhân, yêu cầu, đặc tả Use Case, biểu đồ hoạt động và lớp nghiệp vụ. Phần thiết kế (sẽ triển khai ở các chương tiếp theo) trình bày kiến trúc, biểu đồ tuần tự, lớp thiết kế, cơ sở dữ liệu và giao diện. Công nghệ định hướng gồm ReactJS, Java, PostgreSQL và Redis.

\section*{6. Bố cục báo cáo}
\phantomsection
\addcontentsline{toc}{section}{6. Bố cục báo cáo}

Báo cáo gồm các phần chính sau:
\begin{itemize}[leftmargin=1.4em]
\item \textbf{Mở đầu:} lý do chọn đề tài, mục tiêu, đối tượng, phạm vi, phương pháp và bố cục.
\item \textbf{Chương 1 -- Giới thiệu đề tài và lựa chọn công nghệ:} giới thiệu đề tài, đối tượng sử dụng, phạm vi hệ thống, quy trình nghiệp vụ tổng quát và định hướng giải pháp công nghệ.
\item \textbf{Chương 2 -- Phân tích hệ thống:} khảo sát nghiệp vụ, phân tích yêu cầu, mô hình Use Case tổng quát và đặc tả từng nhóm chức năng từ UC01 đến UC10.
\item \textbf{Kết luận và hướng phát triển:} tóm tắt kết quả đã đạt được và định hướng hoàn thiện.
\item \textbf{Tài liệu tham khảo} và \textbf{Phụ lục}.
\end{itemize}
"""

CONCLUSION = r"""
\clearpage
\chapter*{KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN}
\phantomsection
\addcontentsline{toc}{chapter}{KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN}

\section*{Kết luận}
\phantomsection
\addcontentsline{toc}{section}{Kết luận}

Báo cáo đã xác định bài toán quản lý vòng đời chỗ ở tại ký túc xá PTIT và giới hạn phạm vi thành mười chức năng, chia theo năm giai đoạn: xem phòng, đặt phòng, thuê phòng, đóng phí và trả phòng. Các quy tắc nghiệp vụ then chốt đã được hệ thống hóa (BR01--BR12), bảo đảm một giường không bị giữ trùng, một sinh viên không có hai hợp đồng còn hiệu lực và các thay đổi trạng thái được thực hiện đồng bộ.

Phần phân tích đã xây dựng danh sách Use Case, ma trận tác nhân -- Use Case và đặc tả chi tiết các chức năng UC03, UC04, UC05, UC06, UC07, UC08, UC09. Định hướng công nghệ được lựa chọn gồm ReactJS cho giao diện, Java cho backend, PostgreSQL cho dữ liệu chính và Redis cho hỗ trợ tra cứu, giữ chỗ tạm.

\section*{Hướng phát triển}
\phantomsection
\addcontentsline{toc}{section}{Hướng phát triển}

Trong các giai đoạn tiếp theo, nhóm sẽ hoàn thiện các mục còn thiếu ở Chương 2 (đặc tả UC01, UC02, UC10 và các sơ đồ lớp, biểu đồ Use Case), sau đó chuyển sang thiết kế kiến trúc, cơ sở dữ liệu, giao diện và cài đặt minh họa luồng dữ liệu từ tạo phòng đến hoàn tất trả phòng.

Các hướng mở rộng gồm tích hợp cổng thanh toán thực tế, thông báo tự động, quản lý điện nước, tài sản, sửa chữa cơ sở vật chất, vi phạm nội trú và đồng bộ với hệ thống đào tạo, trên cơ sở vẫn giữ nguyên các ràng buộc toàn vẹn dữ liệu đã phân tích.
"""

REFERENCES = r"""
\clearpage
\chapter*{TÀI LIỆU THAM KHẢO}
\phantomsection
\addcontentsline{toc}{chapter}{TÀI LIỆU THAM KHẢO}

\begin{enumerate}[leftmargin=1.8em]
\item Nguyễn Văn Vy, Nguyễn Văn Hòa, \textit{Phân tích thiết kế hệ thống thông tin}, NXB Giáo dục Việt Nam.
\item Nguyễn Văn Ba, \textit{Phân tích và thiết kế hệ thống thông tin}, NXB Đại học Quốc gia Hà Nội.
\item Booch, G., Rumbaugh, J., Jacobson, I., \textit{The Unified Modeling Language User Guide}, Addison-Wesley.
\item React, \textit{React documentation}, \url{https://react.dev/}.
\item Oracle, \textit{Java documentation}, \url{https://docs.oracle.com/en/java/}.
\item PostgreSQL Global Development Group, \textit{PostgreSQL documentation}, \url{https://www.postgresql.org/docs/}.
\item Redis Ltd., \textit{Redis documentation}, \url{https://redis.io/docs/}.
\end{enumerate}
"""

APPENDIX = r"""
\clearpage
\chapter*{PHỤ LỤC}
\phantomsection
\addcontentsline{toc}{chapter}{PHỤ LỤC}

\section*{PHỤ LỤC A. Danh sách Use Case}
\phantomsection
\addcontentsline{toc}{section}{PHỤ LỤC A. Danh sách Use Case}

Mười chức năng trong phạm vi đề tài: UC01 Tạo phòng và giường; UC02 Tìm phòng còn chỗ phù hợp; UC03 Gửi yêu cầu đặt phòng; UC04 Giữ phòng và giường; UC05 Lập hợp đồng thuê phòng; UC06 Xác nhận bàn giao phòng; UC07 Phát hành khoản phí nội trú theo kỳ; UC08 Thanh toán khoản phí nội trú; UC09 Gửi yêu cầu trả phòng; UC10 Xác nhận hoàn tất trả phòng.

\section*{PHỤ LỤC B. Quy tắc nghiệp vụ chung}
\phantomsection
\addcontentsline{toc}{section}{PHỤ LỤC B. Quy tắc nghiệp vụ chung}

Các quy tắc BR01--BR12 được trình bày tại Mục 2.1.6, Chương 2.

\section*{PHỤ LỤC C. Các sơ đồ UML}
\phantomsection
\addcontentsline{toc}{section}{PHỤ LỤC C. Các sơ đồ UML}

Các sơ đồ Use Case tổng quát, sơ đồ lớp và biểu đồ hoạt động sẽ được tập hợp tại phụ lục này khi hoàn thiện mô hình.
"""

WORK = r"""
\clearpage
\chapter*{BẢNG PHÂN CÔNG CÔNG VIỆC CÁC THÀNH VIÊN}
\phantomsection
\addcontentsline{toc}{chapter}{BẢNG PHÂN CÔNG CÔNG VIỆC CÁC THÀNH VIÊN}

Theo phân công trong danh sách Use Case:

\begin{table}[H]
\centering
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{0.14\textwidth}|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}p{0.22\textwidth}|>{\raggedright\arraybackslash}p{0.18\textwidth}|}
\hline
\textbf{Mã} & \textbf{Use Case} & \textbf{Tác nhân} & \textbf{Phụ trách} \\
\hline
UC01 & Tạo phòng và giường & Cán bộ & Tùng \\
\hline
UC02 & Tìm phòng còn chỗ phù hợp & Sinh viên & Tùng \\
\hline
UC03 & Gửi yêu cầu đặt phòng & Sinh viên & Nhân \\
\hline
UC04 & Giữ phòng và giường cho sinh viên & Cán bộ & Nhân \\
\hline
UC05 & Lập hợp đồng thuê phòng cho sinh viên & Cán bộ & Huân \\
\hline
UC06 & Xác nhận bàn giao phòng cho sinh viên & Cán bộ & Huân \\
\hline
UC07 & Phát hành khoản phí nội trú theo kỳ & Cán bộ & Tuấn \\
\hline
UC08 & Thanh toán khoản phí nội trú & Sinh viên & Tuấn \\
\hline
UC09 & Gửi yêu cầu trả phòng & Sinh viên & Dũng \\
\hline
UC10 & Xác nhận hoàn tất trả phòng & Cán bộ & Dũng \\
\hline
\end{tabularx}
\caption{Phân công phụ trách các Use Case}
\label{tab:work-assignment}
\end{table}
"""


def main() -> None:
    text = MD.read_text(encoding="utf-8")
    body = re.split(r"\n(?=\[image\d+\]:)", text)[0]
    body = body.replace("\\.", ".")
    lines = body.splitlines()
    files = convert_body(lines)
    ch1 = add_placeholders(files["ch1"])
    ch2 = add_placeholders(files["ch2"])
    (ROOT / "chapters" / "chapter1.tex").write_text("\n".join(ch1).strip() + "\n", encoding="utf-8")
    (ROOT / "chapters" / "chapter2.tex").write_text("\n".join(ch2).strip() + "\n", encoding="utf-8")
    (ROOT / "frontmatter" / "introduction.tex").write_text(INTRO.lstrip("\n"), encoding="utf-8")
    (ROOT / "chapters" / "conclusion.tex").write_text(CONCLUSION.lstrip("\n"), encoding="utf-8")
    (ROOT / "chapters" / "references.tex").write_text(REFERENCES.lstrip("\n"), encoding="utf-8")
    (ROOT / "appendices" / "appendix.tex").write_text(APPENDIX.lstrip("\n"), encoding="utf-8")
    (ROOT / "appendices" / "work_assignment.tex").write_text(WORK.lstrip("\n"), encoding="utf-8")
    print("Wrote chapter1", len(ch1), "lines")
    print("Wrote chapter2", len(ch2), "lines")


if __name__ == "__main__":
    main()
