import pickle

def Parse_Name(d):
    """ Parses station, side, layer and sector
    from a unique sector name """
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f)
    if d in NameList['TTNames']:
        return {'side':d[4:11],'layer':d[0:4],'sector':d[17:],'station':''}
    if d in NameList['ITNames']:
        station = d[0:3]
        sides = {'A':'ASide', 'B':'Bottom', 'C':'CSide', 'T':'Top'}
        side = sides[d[3]]
        layer = d[3+len(side):3+len(side)+1]
        if layer=='X':
            layer = d[3+len(side):3+len(side)+2]
        sector = str(d[len(d)-1])
        return {'station':station,'side':side,'layer':layer,'sector':sector}
    return d
