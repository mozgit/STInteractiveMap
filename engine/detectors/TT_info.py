"""
These functions define position and drawing style of every single element of TT.
"""

def TT_reg_len(det,region):
    top = 25
    if ((det[2]=='a') and (region == 'RegionB')):
        top = 19
    if ((det[2]=='b') and (region == 'RegionB')):
        top = 27
    return range(1, top)


def TT_div_info(det, region, sector):
    nX = 6
    nY = 4
    sector_iy = sector-1
    sector_ix = sector-1
    if ((det[2]=='a') and (region == 'RegionB')):
        nX = 3
        nY = 6
    if ((det[2]=='b') and (region == 'RegionB')):
        nX = 5
        if ((sector>4) and (sector<23)):
            sector_iy = sector+1
            sector_ix = sector+1
            nY = 6
        if (sector>22):
            sector_iy = sector-7
            sector_ix = sector-7

    width = str(float(100*1./nX))+"%"
    height = str(float(100*1./nY))+"%"
    top = str(float(100*1./nY)*(nY-sector_iy%nY-1))+"%"
    left = str(float(100*1./nX)*(nX-int((sector_ix-sector_ix%nY)/nY)-1))+"%"
    return {'width':width, 
            'height':height, 
            'top':top, 
            'left':left,
            'position':'absolute',
            'border':' 1px solid #000000',
            'text-align':'center'}


def TT_layer_info(a):
    if a == 'TTaU':
        return {'position':'absolute',
                'top': '0%',
                'left': '0%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    if a == 'TTaX':
        return {'position':'absolute',
                'top': '0%',
                'left': '50%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    if a == 'TTbV':
        return {'position':'absolute',
                'top': '50%',
                'left': '0%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    if a == 'TTbX':
        return {'position':'absolute',
                'top': '50%',
                'left': '50%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    return {}


def TT_side_info(a,r):
    if (r == 'RegionA'): return {'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 0%',
                                'width':'32%',
                                'height':'99%'}

    if (r == 'RegionB'): return {'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 33.3%',
                                'width':'32%',
                                'height':'99%'}

    if (r == 'RegionC'): return {'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 66.6%',
                                'width':'32%',
                                'height':'99%'}
    return {}