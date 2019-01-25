PDF = kalman.pdf
DVI = kalman.dvi
TEX = kalman.tex

TEX_PATH = /cygdrive/c/w32tex/bin64
PDF_PATH = /cygdrive/c/w32tex/share/texworks
PLATEX = $(TEX_PATH)/platex
DVIPDFMX = $(TEX_PATH)/dvipdfmx
PDFOPEN = $(PDF_PATH)/texworks

.PHONY: clean view

all: view

view: $(PDF)
	$(PDFOPEN) $^ &

$(PDF): $(DVI)
	$(DVIPDFMX) $^

# 必ずしも latex 2回やる必要はないが判定が難しい
# latex 処理時 の warning が出なかったら2回やるという手がある?
$(DVI): $(TEX)
	$(PLATEX) $< && $(PLATEX) $<

clean:
	rm -rf *.aux *.log *.toc *.dvi *.bbl *.blg *~
