TEX=main.tex

all:
	latexmk $(TEX)

watch:
	latexmk -pvc $(TEX)

clean:
	latexmk -c $(TEX)

distclean:
	latexmk -C $(TEX)

.PHONY: all watch clean distclean
