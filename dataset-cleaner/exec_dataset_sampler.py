import pandas
import numpy
import sys
from argparse import ArgumentParser

def dataset_sampler(inp_file_loc,interval_freq,max_sent,encode,tot_max):
	try:
		df=pandas.read_csv(inp_file_loc,encoding=encode)
	except:
		print("file error : pls provide valid file (or) change the encoding !")
		sys.exit(1)
	try:
		if tot_max is None :
			tot_max=df["score_out"].max()
	except:
		print("col. error : cannot find 'score_out' column inside the file !")
		sys.exit(1)
	df1=pandas.DataFrame(columns=["src_out","tgt_out","score_out"])
	counter=0
	listx=numpy.arange(float(tot_max),1.0,-(interval_freq))
	for i in listx:
		for x,y in df.iterrows():
			if counter == max_sent:
				break
			if y["score_out"] >= i-interval_freq :
				if y["score_out"] < i :
					df1=df1.append({"src_out":y["src_out"],"tgt_out":y["tgt_out"],"score_out":y["score_out"]},ignore_index=True)
					counter+=1
		print("%.2f" % i,"-","%.2f" % float(i-interval_freq),": Done with",counter,"counts")
		counter=0
	new_file_loc=inp_file_loc[:inp_file_loc.find(".")]+"-sampled.csv"
	print("Total no. of sentences =",df1.shape[0])
	df1.to_csv(new_file_loc,encoding=encode,index=False,)

def main():
	parser = ArgumentParser()
	parser.add_argument("-f","--inp-file", help="Input File Location",type=str, default="./")
	parser.add_argument("-i","--interval", help="frequency interval (default=0.5)", type=float, default=0.5)
	parser.add_argument("-e","--encoding", help="encoding (default='utf-16')", type=str, default="utf-16")
	parser.add_argument("-s","--max-sentences", help="max sentences per interval (default=15)", type=int, default=15)
	parser.add_argument("-c","--max-cutoff", help="max value for cutoff", type=float, default=None)
	args = parser.parse_args()
	cutoff=args.max_cutoff
	inp_file_loc=args.inp_file
	encode=args.encoding
	interval_freq=args.interval
	max_sent=args.max_sentences
	dataset_sampler(inp_file_loc,interval_freq,max_sent,encode,cutoff)
	
if __name__ == "__main__":
	main()
