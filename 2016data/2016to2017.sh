python 2016to2017.py train > train.2016to2017.conll.iob
python 2016to2017.py dev > dev.2016to2017.conll.iob
python 2016to2017.py test > test.2016to2017.conll.iob

cat train.2016to2017.conll.iob dev.2016to2017.conll.iob > train.2016.final
cat test.2016to2017.conll.iob > test.2016.final

#cat train.2016to2017.conll.iob ../data/split/train.conll.iob > train.cat.iob
#cat dev.2016to2017.conll.iob ../data/split/dev.conll.iob > dev.cat.iob
#cat test.2016to2017.conll.iob ../data/split/test.conll.iob > test.cat.iob
#cat train.cat.iob test.2016to2017.conll.iob > train.catt.iob
#cat train.catt.iob dev.2016to2017.conll.iob > train.cattt.iob

