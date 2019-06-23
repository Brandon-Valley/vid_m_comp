from PIL import Image
#  
# img = Image.new('RGB', (2000, 2000), color = (0,255,0))
# img.save('green.png')
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw



def drawTextWithOutline(text, x, y, font, draw):
    draw.text((x-2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y+2), text,(0,0,0),font=font)
    draw.text((x-2, y+2), text,(0,0,0),font=font)
    draw.text((x, y), text, (255,255,255), font=font)
    return


def make_lines(text, font, img_w, draw):
    def _cut_last_word(line):
#         print('in _cut_last_word, about to cut line: ', line)#````````````````````````````````````````````````````````````
        split_line_str_l = line.split(' ')
        
        if len(split_line_str_l) == 1:
            return False
#             raise Exception('ERROR:  single word in text is wider than image: ', text)
        
        new_line = ''
        for word in split_line_str_l[0:-1]:
            new_line += word + ' '
        return new_line[0:-1] # remove extra space at end

    lines = []
    
    while(len(text) > 0):
        test_line = text
#         print('above while')#````````````````````````````````````````````````````````````````````````````````````````````
        
        # while the length of the line is wider than the image
        while(draw.textsize(test_line, font)[0] > img_w):
#             print('test_line: ', test_line)#````````````````````````````````````````````````````
#             print('  draw.textsize(test_line, font)[0]: ', draw.textsize(test_line, font)[0])#`````````````````````````
            cut_line = _cut_last_word(test_line)
#             print('    cut_line: ', cut_line)#```````````````````````````````````````````````````````````````````
            
            # if there is 1 word that is wider than image
            if cut_line == False:
                break
            else:
                test_line = cut_line
                
#             print('end of while test_line: ', test_line)#````````````````````````````````````````````````````
#             print(' ')

        lines.append(test_line)
        text = text[len(test_line):]
    return lines



def drawText(text, pos, font, img, draw):
    text = text.upper()
    
    img_w, img_h = img.size
#     print('img_w: ', img_w)#```````````````````````````````````````````````````````````````````
    
    lines = make_lines(text, font, img_w, draw)
#     print('lines (final): ', lines)#`````````````````````````````````````````````````````````````````````
    
    w, h = draw.textsize(text, font) # measure the size the text will take
#     lines = [text]
    lineCount = len(lines)

#     lineCount = 1
#     if w > img.width:
#         lineCount = int(round((w / img.width) + 1))
# 
#     print("lineCount: {}".format(lineCount))
# 
#     lines = []
#     if lineCount > 1:
#   
#         lastCut = 0
#         isLast = False
#         for i in range(0,lineCount):
#             if lastCut == 0:
#                 cut = (len(text) / lineCount) * i
#             else:
#                 cut = lastCut
#   
#             if i < lineCount-1:
#                 nextCut = (len(text) / lineCount) * (i+1)
#             else:
#                 nextCut = len(text)
#                 isLast = True
#                   
#             nextCut = int(nextCut)
#             cut = int(cut)
#   
#             print("cut: {} -> {}".format(cut, nextCut))
#   
#             # make sure we don't cut words in half
#               
#             print('nextCut: ', nextCut, type(nextCut))#```````````````````````````````````````````````````
#             if nextCut == len(text) or text[nextCut] == " ":
#                 print("may cut")
#             else:
#                 print("may not cut")
#                 print(text, nextCut, type(nextCut), len(text))#````````````````````````````````````````````````````````````````````
#                 while text[nextCut] != " ":
#                     nextCut += 1
#                 print("new cut: {}".format(nextCut))
#   
#             line = text[cut:nextCut].strip()
#   
#             # is line still fitting ?
#             w, h = draw.textsize(line, font)
#             if not isLast and w > img.width:
#                 print("overshot")
#                 nextCut -= 1
#                 while text[nextCut] != " ":
#                     nextCut -= 1
#                 print("new cut: {}".format(nextCut))
#   
#             lastCut = nextCut
#             lines.append(text[cut:nextCut].strip())
#   
#     else:
#         lines.append(text)
#   
#     print(lines)

    lastY = -h
    if pos == "bottom":
        lastY = img.height - h * (lineCount+1) - 10

    for i in range(0, lineCount):
#     print(i)#````````````````````````````````````````````````````````````````````````````````````
        w, h = draw.textsize(lines[i], font)
        x = img.width/2 - w/2
        y = lastY + h
        drawTextWithOutline(lines[i], x, y, font, draw)
        lastY = y


def add_caption(in_img_path, out_img_path, top_text, bottom_text):
    img  = Image.open(in_img_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", 80)

    drawText(top_text,    "top",    font, img, draw)
    drawText(bottom_text, "bottom", font, img, draw)
    
    img.save(out_img_path)


if __name__ == '__main__':  
    add_caption('pics/test_thumb.png', 'pics/t2.png', 'dhllllllllllllllllllloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo', 'dhl kkkkk kkk aaaaaaa iiiiiiiiiii bbbbbbbbbb nnnnnnnnnnnzzzzzzz ggggggggggg')

