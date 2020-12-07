import json
import codecs

# example of input format
#[
#Explicit|||98..105||instead||2|instead|||Expansion|||||||||||37..67|1|That's where things went wrong||||||||69..97|2|I should have eaten a carrot|||||||||||||
#Explicit|||15..22||because||0|because|||Contingency|||||||||||0..14|0|I ate a banana||||||||23..35|0|I was hungry|||||||||||||
#]


# example of output format
#[
#{'ID': 1, 'DocID': '06-08-2020_17:29:47', 'Sense': 'Contingency.Cause.Reason', 'Type': 'Explicit', 'Arg1': {'CharacterSpanList': [], 'RawText': '', 'TokenList': []}, 'Arg2': {'CharacterSpanList': [[73, 271]], 'RawText': 'der dramatischen Kassenlage in Brandenburg hat sie jetzt eine seit mehr als einem Jahr erarbeitete Kabinettsvorlage überraschend auf Eis gelegt und vorgeschlagen , erst 2003 darüber zu entscheiden .', 'TokenList': [[73, 76, 14, 1, 2], [77, 89, 15, 1, 3], [90, 100, 16, 1, 4], [101, 103, 17, 1, 5], [104, 115, 18, 1, 6], [116, 119, 19, 1, 7], [120, 123, 20, 1, 8], [124, 129, 21, 1, 9], [130, 134, 22, 1, 10], [135, 139, 23, 1, 11], [140, 144, 24, 1, 12], [145, 148, 25, 1, 13], [149, 154, 26, 1, 14], [155, 159, 27, 1, 15], [160, 171, 28, 1, 16], [172, 188, 29, 1, 17], [189, 201, 30, 1, 18], [202, 205, 31, 1, 19], [206, 209, 32, 1, 20], [210, 216, 33, 1, 21], [217, 220, 34, 1, 22], [221, 234, 35, 1, 23], [235, 236, 36, 1, 24], [237, 241, 37, 1, 25], [242, 246, 38, 1, 26], [247, 254, 39, 1, 27], [255, 257, 40, 1, 28], [258, 269, 41, 1, 29], [270, 271, 42, 1, 30]]}, 'Connective': {'CharacterSpanList': [[63, 72]], 'RawText': 'Auf Grund', 'TokenList': [[63, 66, 12, 1, 0], [67, 72, 13, 1, 1]]}}
#]


def pipe2json(docid, inp, ptreecsv):

    token2offsets = parse_ptreecsv(ptreecsv)

    l = []
    for i, line in enumerate(inp):
        parts = line.split('|')
        assert len(parts) == 48
        arg1spanlist = []
        if parts[22]:
            arg1spanlist = [[int(x.split('..')[0]), int(x.split('..')[1])] for x in parts[22].split(';')]
        arg1tokenlist = spanlist2tokenlist(arg1spanlist, token2offsets)
        arg1 = {'CharacterSpanList': arg1spanlist,
                'RawText': parts[24],
                'TokenList': arg1tokenlist
        }
        arg2spanlist = []
        if parts[32]:
            arg2spanlist = [[int(x.split('..')[0]), int(x.split('..')[1])] for x in parts[32].split(';')]
        arg2tokenlist = spanlist2tokenlist(arg2spanlist, token2offsets)
        arg2 = {'CharacterSpanList': arg2spanlist,
               'RawText': parts[34],
               'TokenList': arg2tokenlist
        }
        connspanlist = []
        if parts[3]:
            connspanlist = [[int(x.split('..')[0]), int(x.split('..')[1])] for x in parts[3].split(';')]
        conntokenlist = spanlist2tokenlist(connspanlist, token2offsets)
        conn = {'CharacterSpanList': connspanlist,
                'RawText': parts[5],
                'TokenList': conntokenlist
        }
        rel = {'ID': i+1, # think in conll pdtb format, relations are 1-based. 
               'DocID': docid,
               'Sense': parts[11],
               'Type': parts[0],
               'Arg1': arg1,
               'Arg2': arg2,
               'Connective': conn
        }
        l.append(rel)

    return l
        

def spanlist2tokenlist(spanlist, token2offsets):

    tokenlist = []
    for span in spanlist:
        start, end = span[0], span[1]
        for token in token2offsets:
            s, e = token2offsets[token]['offsets'].split('..')
            s, e = int(s), int(e)
            if s >= start and e <= end:
                tokenlist.append([s, e, token, token2offsets[token]['sid'], token2offsets[token]['stid']])
    return tokenlist
        

def parse_ptreecsv(pcsv):

    token2offsets = {}
    sid = 0
    tid = 0
    for i, line in enumerate(codecs.open(pcsv).readlines()):
        p = line.strip().split(',')
        t = p[-1]
        offsets = p[-2]
        if not int(p[1]) == sid:
            sid = int(p[1])
            tid = 0
        token2offsets[i] = {'token': t, 'sid': sid, 'stid': tid, 'offsets': offsets}
        tid += 1
    return token2offsets
            

    
