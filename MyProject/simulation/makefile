TEX = report
TARGET = report

.PHONY: clean debug gvshow pdfshow acroshow dvishow

#LATEX = pdflatex

#$(TARGET).pdf: $(TARGET).ps
#	ps2pdf $(TARGET).ps

#$(TARGET).ps: $(TARGET).dvi
#	dvips -o $(TARGET).ps $(TARGET).dvi

$(TARGET).pdf: $(TEX).tex
	pdflatex $(LATEX_ARGS) $(TEX)

#$(TARGET).dvi: $(TEX).tex
#	$(LATEX) $(TEX).tex
#	@mv $(TEX).dvi $(TARGET).dvi
force:
	pdflatex $(LATEX_ARGS) $(TEX)

clean:
	rm *.aux *.log

debug:
	latex $(TEX).tex

gvshow: $(TARGET).ps
	gv $(TARGET).ps

pdfshow: $(TARGET).pdf
	xpdf $(TARGET).pdf

acroshow: $(TARGET).pdf
	acroread $(TARGET).pdf

dvishow: $(TARGET).dvi
	xdvi $(TARGET).dvi
