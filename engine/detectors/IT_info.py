"""
These functions define position and drawing style of every single element of IT.
"""

def IT_station_info(st):
    if st == 'IT1': return{'position':'absolute',
                            'top': '0%',
                            'left': '0%',
                            'width':'100%',
                            'height':'33.3%',
                            'border':'1px dashed',
                            'text-align':'left'}
    if st == 'IT2': return{'position':'absolute',
                            'top': '33.3%',
                            'left': '0%',
                            'width':'100%',
                            'height':'33.3%',
                            'border':'1px dashed',
                            'text-align':'left'}
    if st == 'IT3': return{'position':'absolute',
                            'top': '66.6%',
                            'left': '0%',
                            'width':'100%',
                            'height':'33.3%',
                            'border':'1px dashed',
                            'text-align':'left'}
    return {}


def IT_side_info(st,s):
    
    if s == 'ASide': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 30%',
                                'left':' 0%',
                                'width':'33.3%',
                                'height':'40%'}
    if s == 'CSide': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 30%',
                                'left':' 66.6%',
                                'width':'33.3%',
                                'height':'40%'}
    if s == 'Bottom': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 60%',
                                'left':' 33.3%',
                                'width':'33.3%',
                                'height':'40%'}
    if s == 'Top': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 33.3%',
                                'width':'33.3%',
                                'height':'40%'}
    return {}


def IT_layer_info(st,s,l):
    if l == 'X1': return {'position':'absolute',
                        'top':' 0%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    if l == 'U': return {'position':'absolute',
                        'top':' 25%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    if l == 'V': return {'position':'absolute',
                        'top':' 50%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    if l == 'X2': return {'position':'absolute',
                        'top':' 75%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    return {}

def IT_div_info(st,s,l,n):
    nX = 7
    width = str(float(1./nX)*100)+"%"
    height = "100%"
    top = "0%"
    left = str(float(nX-n)/nX*100)+"%"
    return {'width':width, 
            'height':height, 
            'top':top, 
            'left':left,
            'position':'absolute',
            'border':'1px solid #000000',
            'text-align':'center'}
