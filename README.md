# Khung báo cáo LaTeX PTIT (Trình biên dịch XeLaTeX)

Thư mục này chứa template LaTeX cho báo cáo PTIT, hỗ trợ hai kiểu báo cáo:

- `TTTN`: Báo cáo thực tập tốt nghiệp.
- `BTL`: Báo cáo bài tập lớn.
> **Lưu ý**: Đây là bản mẫu biên dịch bằng **XeLaTeX**. Báo cáo dùng `Times New Roman` nếu font đã được cài đặt; nếu chưa có, tự chuyển sang `Liberation Serif` và `Liberation Sans`. Nếu bạn muốn biên dịch bằng **pdfLaTeX** (mặc định trên Overleaf và TeX thông thường), vui lòng sử dụng bản mẫu tại [pdflatex_report_template](../pdflatex_report_template).


## Cấu trúc thư mục

- `main.tex`: file chính để biên dịch báo cáo.
- `config.tex`: cấu hình thông tin trường, khoa, giảng viên, sinh viên, lớp, nhóm, năm và loại báo cáo.
- `frontmatter/`: bìa, nhận xét, lời cảm ơn.
- `chapters/`: mở đầu, các chương, kết luận, tài liệu tham khảo.
- `appendices/`: phụ lục và bảng phân công.
- `assets/`: ảnh dùng trong báo cáo, gồm khung bìa và logo PTIT.

## Cấu hình thông tin báo cáo

Sửa các biến trong `config.tex` trước khi biên dịch:

```tex
\newcommand{\ReportTemplateType}{TTTN} % Chọn TTTN hoặc BTL
\newcommand{\AuthorName}{...}
\newcommand{\ClassName}{...}
\newcommand{\StudentName}{...}
\newcommand{\StudentID}{...}
```

`ReportTemplateType` điều khiển header/footer:

- `TTTN`: header trái là `Báo cáo thực tập tốt nghiệp`, header phải là tên phần hiện tại như `Lời mở đầu`, `Chương 1`, `Kết luận`; footer trái là `Tên sinh viên - Lớp`, footer phải là số trang; có đường kẻ ở header và footer.
- `BTL`: header phải là `Chương [X] - [Tên chương]`, footer phải là số trang; không có đường kẻ header/footer.

## Format trình bày báo cáo

Template đang cấu hình các quy cách trình bày chính trong `main.tex`:

- Khổ giấy: A4.
- Lề: trái `3.0cm`, phải `2.0cm`, trên `2.0cm`, dưới `2.0cm`.
- Font nội dung: `Times New Roman`, hoặc `Liberation Serif` khi Times New Roman chưa được cài đặt.
- Cỡ chữ nội dung: `12pt`.
- Giãn dòng: `1.15`.
- Thụt đầu dòng: `1.25cm`.
- Khoảng cách đoạn: `0pt`.
- Căn lề: LaTeX mặc định căn đều hai lề cho nội dung văn bản.
- Header/footer: cỡ chữ `10pt`.
- Với `TTTN`: header và footer đều có đường kẻ; footer trái là `Tên sinh viên - Lớp`, footer phải là số trang.
- Với `BTL`: footer phải là số trang; header phải là `Chương [X] - [Tên chương]`.
- Tiêu đề chương hiển thị cùng dòng, ví dụ: `CHƯƠNG 1. CƠ SỞ LÝ THUYẾT`.
- Trong mục lục, chương hiển thị rõ dạng `Chương 1 CƠ SỞ LÝ THUYẾT`.
- `MỤC LỤC` được đưa vào chính mục lục.
- Trang `NHẬN XÉT, ĐÁNH GIÁ, CHO ĐIỂM` không được đưa vào mục lục.
- Tên bảng đặt phía trên bảng bằng `\caption{...}` trong môi trường `table`.
- Tên hình đặt phía dưới hình bằng `\caption{...}` trong môi trường `figure`.

Khi thay đổi mục lục, danh mục hình hoặc danh mục bảng, cần biên dịch ít nhất hai lượt để số trang và danh mục cập nhật đúng.

## Checklist trước khi nộp

### Nội dung

- [ ] Tên đề tài trên bìa, mục lục và nội dung thống nhất.
- [ ] Có đầy đủ các phần bắt buộc.
- [ ] Mở đầu nêu rõ lý do, mục tiêu, đối tượng, phạm vi và phương pháp.
- [ ] Nội dung chính có cơ sở lý thuyết, phân tích, triển khai và đánh giá.
- [ ] Kết luận tóm tắt đúng kết quả đã đạt được.
- [ ] Hướng phát triển phù hợp với hạn chế.
- [ ] Tài liệu tham khảo có thật và được trích dẫn đúng.
- [ ] Phụ lục, nếu có, được đánh số rõ ràng.
- [ ] Bảng phân công công việc rõ ràng nếu làm theo nhóm.

### Trình bày

- [ ] Khổ giấy A4.
- [ ] Lề trái 3.0cm; lề phải/trên/dưới 2.0cm.
- [ ] Font Times New Roman.
- [ ] Cỡ chữ nội dung 12 hoặc 13.
- [ ] Căn đều hai lề.
- [ ] Giãn dòng 1.1 đến 1.2.
- [ ] Header và footer thống nhất.
- [ ] Số trang đúng quy định.
- [ ] Tiêu đề, mục, tiểu mục đánh số thống nhất.
- [ ] Bảng có tên phía trên.
- [ ] Hình có tên phía dưới.
- [ ] Các hình/bảng có nguồn nếu không tự tạo.
- [ ] Mục lục, danh mục bảng và danh mục hình đã cập nhật.

### Ngôn ngữ

- [ ] Không sai chính tả.
- [ ] Không dùng văn nói.
- [ ] Không viết câu quá dài.
- [ ] Không dùng từ viết tắt khi chưa giải thích.
- [ ] Không sao chép nguyên văn tài liệu không trích dẫn.
- [ ] Thuật ngữ chuyên môn được dùng thống nhất.

## Cách chạy

Cách nhanh nhất:

```bash
make
```

Hoặc chạy trực tiếp:

```bash
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
```

Nếu không dùng `latexmk`, có thể chạy XeLaTeX trực tiếp. Nên chạy ít nhất hai lượt khi thay đổi mục lục:

```bash
xelatex -interaction=nonstopmode -file-line-error main.tex
xelatex -interaction=nonstopmode -file-line-error main.tex
```

File PDF đầu ra: `main.pdf`.

## Header theo từng phần TTTN

Với `TTTN`, header phải được đặt trong `main.tex` bằng macro:

```tex
\StartReportSection{Lời mở đầu}
\input{chapters/introduction.tex}

\StartReportSection{Chương 1}
\input{chapters/chapter1.tex}
```

Khi thêm chương hoặc phần mới, thêm `\StartReportSection{...}` ngay trước `\input{...}` tương ứng.

## Thay ảnh / placeholder

Trong `main.tex` có macro an toàn:

```tex
\imageorplaceholder[0.7\textwidth]{assets/ten_anh.png}{Mô tả ảnh}
```

Nếu file ảnh không tồn tại, LaTeX sẽ tự hiển thị khung `PLACEHOLDER HÌNH ẢNH` thay vì dừng biên dịch.

Để tạo hình chờ trong nội dung chương:

```tex
\placeholderfigure{Tên hình cần bổ sung}
```
