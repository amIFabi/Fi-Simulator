import sys, subprocess, os, json, base64

def openFile(fileName="../sim/simulation.png"):
	if(sys.platform.startswith("darwin")):
		subprocess.call(("open", fileName))
	elif(os.name == "nt"):
		os.startfile(fileName)
	elif(os.name == "posix"):
		subprocess.call(("xdg-open", fileName))

def writeJSON(fileName, data):
	filePath = fileName + ".json"
	with open(filePath, "w") as fp:
		json.dump(data, fp)
	
def imageToString(imageName):
	with open(imageName, "rb") as imageFile:
		base64Str = base64.b64encode(imageFile.read())

	return base64Str

def stringToImage(base64String, fileName):
	fh = open(fileName, "wb")
	fh.write(base64.b64decode(base64String))
	fh.close()

def loadSettings(fileName):
	name = fileName.split(".")[0] + ".png"
	with open(fileName) as json_file:
		data = json.load(json_file)

	b = data["img"].split("'")
	stringToImage(b[1], name)

	return data

def writePrintable(tf, project, evolDict):
	tf.write("\\documentclass[12pt, letterpaper]{article} \n")
	tf.write("\\usepackage{graphicx} \n")
	tf.write("\\usepackage{hyperref} \n")
	tf.write("\\usepackage[utf8]{inputenc} \n")
	tf.write("\\usepackage{float} \n")
	tf.write("\\usepackage{geometry} \n")
	tf.write("\\usepackage{enumitem, array} \n")
	tf.write("\\usepackage{longtable} \n")
	tf.write("\\usepackage{lscape} \n")
	tf.write("\\usepackage[export]{adjustbox} \n")
	tf.write("\\geometry{letterpaper, left=10mm, right=10mm, bottom=20mm, top=20mm} \n")
	# tf.write("\\graphicspath{ {./" + project + "/} } \n")
	tf.write("\\graphicspath{ {" + project + "} } \n")
	tf.write("\\renewcommand{\\rule}{Rule " + evolDict["rule"] + "} \n")
	tf.write("\\renewcommand{\\r}{" + evolDict["rule"] + "} \n")
	tf.write("\\title{ \\rule report} \n")
	tf.write("\\author{Fi } \n")
	tf.write("\\begin{document} \n")
	tf.write("\\begin{titlepage} \n")
	tf.write("\\maketitle \n")
	tf.write("\\tableofcontents \n")
	tf.write("\\end{titlepage} \n")
	tf.write("\\clearpage \n")
	tf.write("\\begin{figure}[H]\n")
	tf.write("  \\centering\n")
	tf.write("  \\includegraphics[height=200mm, width=200mm, keepaspectratio]{simAnalysis.png} \n")
	tf.write("   \\caption{\\rule evolution} \n")
	tf.write("\\end{figure}\n")
	tf.write("\\begin{table}[H]\n")
	tf.write("  \\centering\n")
	tf.write("  \\begin{tabular}{|c|c|c|c| }\n")
	tf.write("     \\hline Seed-Density & Fill & Length & Steps \\\\ \n")
	tf.write("      \\hline " + evolDict["seed"] + " & " + evolDict["fill"] + " & " + evolDict["length"] + " & " + evolDict["steps"] + " \\\\ \n")
	tf.write("      \\hline \n")
	tf.write("       \\end{tabular} \n")
	tf.write("      \\caption{Simulation data} \n")
	tf.write("    \\end{table} \n")

def writeGenotipico(tf, project, optDict, evolDict):
	tf.write("	\\begin{section}{Genotypic Analysis} \n")
	if optDict["meanfield"]:
		with open("../img/MeanField/Regla" + evolDict["rule"] + ".json", 'r') as f:
			datos = json.load(f)
		f.close()
		tf.write("	\\begin{subsection}{Mean Field Theory}\n")
		tf.write("	\\begin{figure}[H]\n")
		tf.write("	\\centering\n")
		tf.write("	\\includegraphics[max width=200mm ,max height=200 mm , keepaspectratio]{../img/MeanField/Plot\\r.png}\n")
		tf.write("  \\caption{\\rule Mean Field Plot}\n")
		tf.write("  \\end{figure}\n")
		tf.write("  \\begin{table}[H]\n")
		tf.write("  \\centering\n")
		tf.write("  \\begin{tabular}{|c|c|c|c|}\n")
		tf.write("  \\hline Rule & Polynomial  & Fixed point & Derivative \\\\ \n")
		#', '.join(a)
		tf.write("  \\hline $\\r$ & $" + datos["Pol0"] + "$  &  $" + datos["Punto"] + "$  & $" + datos["Derivada"] + "$ \\\\  \\hline \n")

def writeFenotipico(tf ,optDict, evolDict, ):
	tf.write("\\begin{section}{Phenotypic Analysis} \n")
  ###### Density
	if optDict["density"]: 
		tf.write("  \\begin{subsection}{Density} \n")
		tf.write("    \\begin{figure}[H] \n")
		tf.write("      \\centering \n")
		tf.write("       \\includegraphics[max width=200mm, max height=200mm, keepaspectratio]{SimDensity.png} \n")
		tf.write("       \\caption{\\rule Density plot} \n")
		tf.write("    \\end{figure} \n")
		tf.write("  \\end{subsection} \n")
  ###### Entropy
	if optDict["entropy"]:
		tf.write("  \\begin{subsection}{Entropy} \n")
		tf.write("    \\begin{figure}[H] \n")
		tf.write("    \\centering \n")
		tf.write("    \\includegraphics[max width=200mm, max height=200mm, keepaspectratio]{SimEntropy.png} \n")
		tf.write("    \\caption{\\rule Entropy plot} \n")
		tf.write("    \\end{figure} \n")
		tf.write("    \\end{subsection}\n")
  ###### Exponente de Lyapunov
	if optDict["lyapunov"]:
		tf.write("    \\begin{subsection}{Lyapunov exponents} \n")
		tf.write("    \\begin{figure}[H] \n")
		tf.write("    \\centering \n")
		tf.write("    \\includegraphics[max width=200mm, max height=200mm, keepaspectratio]{SimDefects.png} \n")
		tf.write("    \\caption{Damage spreading} \n")
		tf.write("    \\end{figure} \n")
		tf.write("    \\end{subsection} \n")
		tf.write("    \\begin{table}[H] \n")
		tf.write("    \\centering \n")
		tf.write("    \\begin{tabular}{cc} \n")
		tf.write("    \\includegraphics[width=70mm, max height=70mm, keepaspectratio]{SimOriginal.png} & \includegraphics[width=70mm, max height=70mm, keepaspectratio]{SimAlter.png} \\ \n")
		tf.write("    \\end{tabular} \n")
		tf.write("    \\caption{Original simulation and Altered simulation comparison \\rule} \n")
		tf.write("    \\end{table} \n")
		tf.write("    \\begin{table}[H] \n")
		tf.write("    \\centering \n")
		tf.write("    \\begin{tabular}{cc} \n")
		tf.write("    \\includegraphics[width=90mm , max height=90mm, keepaspectratio]{LyapunovExp.png} & \includegraphics[width=90mm , max height=90mm, keepaspectratio]{LyapunovExpNorm.png} \\ \n")
		tf.write("    \\end{tabular} \n")
		tf.write("    \\caption{Defects and Lyapunov profile} \n")
		tf.write("    \\end{table} \n")
		#tf.write("    \\end{subsection} \n")
  
	tf.write("    \\end{section} \n")
	tf.write("    \\clearpage \n")

def write(project, optDict, evolDict):
	tf = open(project + ".tex", 'w')

	writePrintable(tf , project, evolDict)
	writeFenotipico(tf, optDict, evolDict)
	writeGenotipico(tf, project, optDict, evolDict)
	tf.write("\\end{document}")
	tf.close()
	os.system('lualatex ' + project + ".tex")
	os.system("rm *.aux *.log *.out *.toc")

def generateReport(path, optDict, evolDict):
	tf = open(path + "Report.tex", 'w')
	tf.write("\\documentclass[12pt, letterpaper]{article} \n")
	tf.write("\\usepackage{graphicx} \n")
	tf.write("\\usepackage{hyperref} \n")
	tf.write("\\usepackage[utf8]{inputenc} \n")
	tf.write("\\usepackage{float} \n")
	tf.write("\\usepackage{geometry} \n")
	tf.write("\\usepackage{enumitem, array} \n")
	tf.write("\\usepackage{longtable} \n")
	tf.write("\\usepackage{lscape} \n")
	tf.write("\\usepackage[export]{adjustbox} \n")
	tf.write("\\geometry{letterpaper, left=10mm, right=10mm, bottom=20mm, top=20mm} \n")
	# tf.write("\\graphicspath{ {./" + project + "/} } \n")
	tf.write("\\graphicspath{ {" + path + "} } \n")
	tf.write("\\renewcommand{\\rule}{Rule " + evolDict["rule"] + "} \n")
	tf.write("\\renewcommand{\\r}{" + evolDict["rule"] + "} \n")
	tf.write("\\title{ \\rule report} \n")
	tf.write("\\author{Fi } \n")
	tf.write("\\begin{document} \n")
	tf.write("\\begin{titlepage} \n")
	tf.write("\\maketitle \n")
	tf.write("\\tableofcontents \n")
	tf.write("\\end{titlepage} \n")
	tf.write("\\clearpage \n")
	tf.write("\\begin{figure}[H]\n")
	tf.write("  \\centering\n")
	tf.write("  \\includegraphics[height=200mm, width=200mm, keepaspectratio]{simAnalysis.png} \n")
	tf.write("   \\caption{\\rule evolution} \n")
	tf.write("\\end{figure}\n")
	tf.write("\\begin{table}[H]\n")
	tf.write("  \\centering\n")
	tf.write("  \\begin{tabular}{|c|c|c|c| }\n")
	tf.write("     \\hline Seed-Density & Fill & Length & Steps \\\\ \n")
	tf.write("      \\hline " + evolDict["seed"] + " & " + evolDict["fill"] + " & " + evolDict["length"] + " & " + evolDict["steps"] + " \\\\ \n")
	tf.write("      \\hline \n")
	tf.write("       \\end{tabular} \n")
	tf.write("      \\caption{Simulation data} \n")
	tf.write("    \\end{table} \n")

	tf.write("\\end{document}")
	tf.close()
	os.system("lualatex " + path + "Report.tex")
	os.system("cp  Report.pdf " + path)
	os.system("rm *.aux *.log *.out *.toc")
	os.system("rm Report.pdf")
	print(path)
