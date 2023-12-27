## Help message
#### Usage: 
```
IMODextract -options -n INPUT_FILE 
```
#### Options:

  -h, --help            show this help message and exit
  
  -c {l,v,u,b,o,n,e,p}, --command {l,v,u,b,o,n,e,p}
                        Choose between 'l'ength, 'v'olume, 'u'nder, 'b'etween,
                        'o'ver, 'n'ame and 'e'xclude, 'p'oint
                        
  -s SELECTED_NAME, --selected_name SELECTED_NAME
                        Name to extract or exclude, depending on c arg. Not
                        case sensitive, can be partial name
                        
  -t THRESHOLD, --threshold THRESHOLD
                        set the minimum number of sections for extraction of
                        object number 'o'ver
                        
  -i INTERVAL [INTERVAL ...], --interval INTERVAL [INTERVAL ...]
                        Interval of the number of layers to extract (e.g. -i 5,20)
                        
  -f FILE_PATH, --file_path FILE_PATH
                        Write full path to the folder containing the file to
                        extract from
                        
  -n INPUT_FILE, --input_file INPUT_FILE
                        Input mod file
                        
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output filename which stores imodinfo results (default = imodinfo_output.txt)

&nbsp;

MAKE SURE YOUR MOD FILE CONTAINS **ONLY** THE OBJECTS AND INFO YOU WANT TO EXTRACT


## Details of -'c'ommand:

-c 'l' and 'v'
  * Effect:  extract the 'l'ength or 'v'olume of all objects in mod file, print a summary (count, mean, std, etc.)
  * Output:  csv file with object number, name and total length/volume + txt file with imodinfo result
  * Usage:   measure skeletons length / 3D objects volume (mitochondria, boutons, etc.)
  * Option required: -n
  * Optional : -o -f

-c 'o' and 'u'
  * Effect: extract object number of all objects whose contours spread on a number of sections equal or superior ('o') or equal or inferior ('u')
of the threshold defined by -t (default = 5 sections)
  * Output: txt file with all object numbers over/under the threshold + txt file with imodinfo result
  * Usage: Can be used to extract a subset of objects based on the number of sections (with imodjoin for example) 
  * Option required: -n
  * Optional : -o -f -t

-c 'b'
  * Effect : extract object number of all objects whose contours spread on a number of sections between the interval defined by -i (ex: -i (5,20))
  * Output : txt file with all object numbers with the interval + txt file with imodinfo result
  * Usage : Can be used to extract a subset of objects based on the number of sections (with imodjoin for example)
  * Option required : -n -i
  * Optional : -o -f

-c 'n' and 'e'
  * Effect : extract object number of all objects whose name include ('n') or don't include ('e') a string of characters defined by -s (ex: -s 'Axon')
  * Output : txt file with all object numbers whose name include characters defined + txt file with imodinfo result
  * Usage : Can be used to extract a subset of objects based on their name (with imodjoin for example)
  * Option required : -n -s
  * Optional : -o -f

-c 'p'
  * Effect : Extract number of point from objects. Objects need to be 'scattered' (Edit -> Object -> Type)
  * Output : csv file with object number, name and number of point per object + txt file with imodinfo result
  * Usage : Can be use to count event/structures marked by scattered point (ex: Synapses)
  * Option required : -n
  * Optional : -o -f
