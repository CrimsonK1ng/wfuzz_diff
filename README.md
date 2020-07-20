# WFUZZ Diff

## Summary

Messing with the idea of using NLP and Image processing to make some efforts with enumerating websites a bit easier. The idea can be summed up in 3 statements:

1. Use simple TFIDF to determine significant difference threshhold in content returned from site
2. Use extremely basic image processing to overlay only the differences between one screenshot and another
3. Try to use both and see what amazing things can happen


## Disclaimer

This is super inneficient, I would not expect this to run well with 100's of returned URL's. That is why I liked the idea of hooking wfuzz into the program. That way you, as the user, can filter the responses to be used in the scanning.


## Use

```bash
usage: main.py [-h] [--baseline BASELINE] {none,nlp,img,both} ...

positional arguments:
  {none,nlp,img,both}
  wfuzz

optional arguments:
  -h, --help           show this help message and exit
  --baseline BASELINE
```


