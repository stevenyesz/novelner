import os
import re
import codecs
from utils import create_dico, create_mapping, zero_digits
from utils import iob2, iob_iobes


def load_sentences(path, lower, zeros):
    """
    Load sentences. A line must contain at least a word and its tag.
    Sentences are separated by empty lines.
    """
    sentences = []
    sentence = []
    ind = 0
    for line in codecs.open(path, 'r', 'utf8'):
        line = zero_digits(line.rstrip()) if zeros else line.rstrip()
        line = line.replace('creative-work','creativework')
        if not line:
            if len(sentence) > 0:
                if 'DOCSTART' not in sentence[0][0]:
                    sentences.append(sentence)
                sentence = []
        else:
            word = line.split()
            if len(word)<6:
                print line,ind,path
            assert len(word) == 6
            sentence.append(word)
        ind += 1
    if len(sentence) > 0:
        if 'DOCSTART' not in sentence[0][0]:
            sentences.append(sentence)
    return sentences


def update_tag_scheme(sentences, tag_scheme):
    """
    Check and update sentences tagging scheme to IOB2.
    Only IOB1 and IOB2 schemes are accepted.
    """
    for i, s in enumerate(sentences):
        tags = [w[-1] for w in s]
        # Check that tags are given in the IOB format
        if not iob2(tags):
            print '-------------------------'
            print s
            s_str = '\n'.join(' '.join(w) for w in s)
            raise Exception('Sentences should be given in IOB format! ' +
                            'Please check sentence %i:\n%s' % (i, s_str))
        if tag_scheme == 'iob':
            # If format was IOB1, we convert to IOB2
            for word, new_tag in zip(s, tags):
                word[-1] = new_tag
        elif tag_scheme == 'iobes':
            new_tags = iob_iobes(tags)
            for word, new_tag in zip(s, new_tags):
                word[-1] = new_tag
        else:
            raise Exception('Unknown tagging scheme!')


def word_mapping(sentences, lower):
    """
    Create a dictionary and a mapping of words, sorted by frequency.
    """
    words = [[x[0].lower() if lower else x[0] for x in s] for s in sentences]
    dico = create_dico(words)
    dico['<UNK>'] = 10000000
    word_to_id, id_to_word = create_mapping(dico)
    print "Found %i unique words (%i in total)" % (
        len(dico), sum(len(x) for x in words)
    )
    return dico, word_to_id, id_to_word


def char_mapping(sentences):
    """
    Create a dictionary and mapping of characters, sorted by frequency.
    """
    chars = ["".join([w[0] for w in s]) for s in sentences]
    dico = create_dico(chars)
    char_to_id, id_to_char = create_mapping(dico)
    print "Found %i unique characters" % len(dico)
    return dico, char_to_id, id_to_char


def tag_mapping(sentences):
    """
    Create a dictionary and a mapping of tags, sorted by frequency.
    """
    tags = [[word[-1] for word in s] for s in sentences]
    dico = create_dico(tags)
    tag_to_id, id_to_tag = create_mapping(dico)
    print "Found %i unique named entity tags" % len(dico)
    return dico, tag_to_id, id_to_tag


def pos_mapping(sentences):
    """
    Create a dictionary and a mapping of pos tags, sorted by frequency.
    """
    tags = [[word[2] for word in s] for s in sentences]
    dico = create_dico(tags)
    tag_to_id, id_to_tag = create_mapping(dico)
    print "Found %i unique POS tags" % len(dico)
    return dico, tag_to_id, id_to_tag


def dep_mapping(sentences):
    """
    Create a dictionary and a mapping of dep tags, sorted by frequency.
    """
    tags = [[word[4] for word in s] for s in sentences]
    dico = create_dico(tags)
    print dico
    tag_to_id, id_to_tag = create_mapping(dico)
    print "Found %i unique Dependency Role tags" % len(dico)
    return dico, tag_to_id, id_to_tag


def ind_mapping(sentences):
    """
    Create a dictionary and a mapping of ind tags, sorted by frequency.
    """
    tags = [[word[1] for word in s] for s in sentences]
    dico = create_dico(tags)
    dico['MAX'] = 10000000 
    print dico
    tag_to_id, id_to_tag = create_mapping(dico)
    print "Found %i unique token Index tags" % len(dico)
    return dico, tag_to_id, id_to_tag


def head_mapping(sentences):
    """
    Create a dictionary and a mapping of head tags, sorted by frequency.
    """
    tags = [[word[3] for word in s] for s in sentences]
    dico = create_dico(tags)
    dico['MAX'] = 10000000 
    print dico
    tag_to_id, id_to_tag = create_mapping(dico)
    print "Found %i unique Head index tags" % len(dico)
    return dico, tag_to_id, id_to_tag


def cap_feature(s):
    """
    Capitalization feature:
    0 = low caps
    1 = all caps
    2 = first letter caps
    3 = one capital (not first letter)
    """
    tmp_state = 0
    if s.lower() == s:
        tmp_state = 0
    elif s.upper() == s:
        tmp_state = 1
    elif s[0].upper() == s[0]:
        tmp_state = 2
    else:
        tmp_state = 3
    if s.startswith('@'):
        tmp_state += 4
    elif s.startswith('#'):
        tmp_state += 8
    #change the number in model.py to 12
    return tmp_state

def prepare_sentence(str_words, word_to_id, char_to_id, lower=False):
    """
    Prepare a sentence for evaluation.
    """
    def f(x): return x.lower() if lower else x

    # str_words_new = []
    # if ('http' in str_words or 'https' in str_words):
    #     ind = str_words_new.index('http')
   # str_words_new = []
   # in_url = False
   # for i in range(len(str_words)):
   #     w = str_words[i]
   #     if 'http' in w:
   #         in_url = True

   #     if in_url:
   #         str_words_new.append('1')
   #         if '/' not in str_words[i:]:
   #             in_url = False
   #     else:
   #         str_words_new.append(w)
   # str_words = str_words_new
    words = [word_to_id[f(w) if f(w) in word_to_id else '<UNK>']
             for w in str_words]
    chars = [[char_to_id[c] for c in w if c in char_to_id]
             for w in str_words]
    caps = [cap_feature(w) for w in str_words]
    # postags = [postag_to_id[]]
    return {
        'str_words': str_words,
        'words': words,
        'chars': chars,
        'caps': caps
    }


def prepare_dataset(sentences, word_to_id, char_to_id, tag_to_id, postag_to_id, dep_to_id, ind_to_id, head_to_id , lower=False):
    """
    Prepare the dataset. Return a list of lists of dictionaries containing:
        - word indexes
        - word char indexes
        - tag indexes
    """
    def f(x): return x.lower() if lower else x
    data = []
    for s in sentences:
        str_words = [w[0] for w in s]
        words = [word_to_id[f(w) if f(w) in word_to_id else '<UNK>']
                 for w in str_words]
        # Skip characters that are not in the training set
        chars = [[char_to_id[c] for c in w if c in char_to_id]
                 for w in str_words]
        caps = [cap_feature(w) for w in str_words]
        tags = [tag_to_id[w[-1]] for w in s]

        postags = [postag_to_id[w[2]] for w in s]
        deps = [dep_to_id[w[4]] for w in s]
        inds = [ind_to_id[w[1] if w[1] in ind_to_id else 'MAX'] for w in s]
        heads = [head_to_id[w[3] if w[3] in head_to_id else 'MAX'] for w in s]

        data.append({
            'str_words': str_words,
            'words': words,
            'chars': chars,
            'caps': caps,
            'tags': tags,
            'postags': postags, 'deps': deps, 'inds': inds, 'heads': heads,
        })
    return data


def augment_with_pretrained(dictionary, ext_emb_path, words):
    """
    Augment the dictionary with words that have a pretrained embedding.
    If `words` is None, we add every word that has a pretrained embedding
    to the dictionary, otherwise, we only add the words that are given by
    `words` (typically the words in the development and test sets.)
    """
    print 'Loading pretrained embeddings from %s...' % ext_emb_path
    assert os.path.isfile(ext_emb_path)

    # Load pretrained embeddings from file
    pretrained = set([
        line.rstrip().split()[0].strip()
        for line in codecs.open(ext_emb_path, 'r', 'utf-8')
        if len(ext_emb_path) > 0 and len(line)>50
    ])
    # We either add every word in the pretrained file,
    # or only words given in the `words` list to which
    # we can assign a pretrained embedding
    if words is None:
        for word in pretrained:
            if word not in dictionary:
                dictionary[word] = 0
    else:
        for word in words:
            if any(x in pretrained for x in [
                word,
                word.lower(),
                re.sub('\d', '0', word.lower())
            ]) and word not in dictionary:
                dictionary[word] = 0

    word_to_id, id_to_word = create_mapping(dictionary)
    return dictionary, word_to_id, id_to_word
