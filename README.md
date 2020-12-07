# LinDocker

Dockerised version of https://github.com/WING-NUS/pdtb-parser, which is in turn based on

Ziheng Lin, Hwee Tou Ng and Min-Yen Kan (2014). A PDTB-Styled End-to-End Discourse Parser. Natural Language Engineering, 20, pp 151-184. Cambridge University Press.

## Usage
- Clone this repository (`git clone https://github.com/PeterBourgonje/GermanShallowDiscourseParser`)
- `cd` into the cloned folder, then build the Docker container (`docker build -t lindocker .`), where `lindocker` is the container name, i.e. can be anything you want, as long as it matches this when running the container.
- After a successful build, start the container (`sudo docker run -p5500:5000 -it lindocker`). This exposes a `parse` endpoint on the specified port.
- The following curl command parses the input file located at `<path/to/local/file.txt>`, and writes the output to `<output.json>`: `curl -X POST -F input=@<path/to/local/file.txt> localhost:5500/parse -o <output.json>`.

Output is returned in CoNLL2016 PDTB format (see [1](https://www.cs.brandeis.edu/~clp/conll16st/dataset.html), [2](https://github.com/attapol/conll16st), [3](https://nbviewer.jupyter.org/github/attapol/conll16st/blob/master/tutorial/tutorial.ipynb)), with the difference being that the CoNLL PDTB format is a text file with each line being a JSON object, whereas this wrapper outputs a proper JSON file (all objects put in a list) for more convenient downstream processing with your JSON library of choice.

The output specifies a DocID property. By default, this is the timestamp of the curl request. The DocID can be specified as input parameter as follows:
`curl -X POST -F input=@<path/to/local/file.txt> localhost:5500/parse?docid=42 -o <output.json>`
