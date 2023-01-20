from flask import Flask, render_template, Response, redirect, url_for
import cv2
import json
# import utils
import numpy as np
import cube_solution_script

app = Flask(__name__)
# camera = cv2.VideoCapture(1)

check1 = 0
check2 = 0
check3=0
check4=0
list_temp = []
current_face="front"

ret_dict_scan=dict()
ret_dict = dict()

ret_scan=dict()
final_scan=dict()
faces = [ "front","right", "back", "left", "top", "bottom"]
for face in faces:
    ret_dict_scan[face] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ret_scan[face] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # final_scan[face] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def html_string_creation(image_name,description):
    str1="""
    <div class="col-lg-4 col-md-6">
                            <div class="nk-gallery-item-box">
        
                                    <img src="static/visual_guide_images/"""



    str3 ="""
                                   
                                    <div class="nk-gallery-item-description">
                                        Seed open don't thing midst created dry every greater divided of, be man is. Second Bring stars fourth gathering he hath face morning fill. Living so second darkness. Moveth were male. May creepeth. Be tree fourth.
                                    </div>
                                </div>
                            </div>"""



    str2 = str1 + image_name
    str2 = str2 + """" alt=""><br>"""
    str2 = str2 + description
    str2 = str2 + str3

    return str2


def generate_frames_scan(colors_range):
    # faces = ["front", "right", "back", "left", "top", "bottom"]
    # for face in faces:
    #     ret_dict_scan[face] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    global faces
    face_iter = iter(faces)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (10, 50)
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 2

    cap = cv2.VideoCapture(1)
    ret = True
    face = next(face_iter)

    global check3
    # check3=check3+1

    if check3>=len(faces)+1:
        return 'hello'
    else:

        while (ret):

            ## read the camera frame
            ret, im = cap.read()
            if not ret:
                break
            else:
                # im = cv2.flip(im, 1)
                frame_width = int(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
                frame_height = int(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

                top_left = (int(frame_width / 3), int(frame_height / 3))
                pcs_width = int(0.05 * frame_width)
                gap = pcs_width
                start_pts = [(top_left[0] + (0.5 * gap), top_left[1] + (0.5 * gap))]

                im = draw_cube_boundry(im, frame_width, frame_height)
                im = cv2.putText(im, 'Scanning faces... Please show ' + face + ' face :: press c to capture', org, font,
                                 fontScale, color, 1, cv2.LINE_AA)
                im = cv2.putText(im, 'if capturing is done properly, press n for the next face, press c to recapture',
                                 (org[0], org[1] + 20), font, fontScale, color, 1, cv2.LINE_AA)

                for h in range(3):
                    for w in range(3):
                        next_start_w = int(start_pts[0][0] + (gap * w * 2))
                        next_start_h = int(start_pts[0][1] + (gap * h * 2))
                        im = cv2.putText(im, str(ret_dict_scan[face][h][2 - w]),
                                         (int(next_start_w + (gap / 2)), int(next_start_h + (gap / 2))), font,
                                         fontScale, (0, 0, 0), 1, cv2.LINE_AA)
                # cv2.imshow("frame", im)
                # pressedKey = cv2.waitKey(1) & 0xFF
                global check4

                if check3==check4:
                    for h in range(3):
                        for w in range(3):
                            next_start_w = int(start_pts[0][0] + (gap * w * 2))
                            next_start_h = int(start_pts[0][1] + (gap * h * 2))

                            piece_val = cv2.mean(im[next_start_h:next_start_h + gap, next_start_w:next_start_w + gap])[:3]
                            min_dist = np.Inf
                            for key in colors_range.keys():
                                clr_range = colors_range[key]
                                dist = abs(piece_val[0] - clr_range[0]) + abs(piece_val[1] - clr_range[1]) + abs(
                                    piece_val[2] - clr_range[2])
                                if (dist < min_dist):
                                    min_dist = dist

                                    ret_dict_scan[face][h][2 - w] = key[0]



                    check4=check3

                if check3>check4:

                    for h in range(3):
                        for w in range(3):
                            next_start_w = int(start_pts[0][0] + (gap * w * 2))
                            next_start_h = int(start_pts[0][1] + (gap * h * 2))

                            piece_val = cv2.mean(im[next_start_h:next_start_h + gap, next_start_w:next_start_w + gap])[:3]
                            min_dist = np.Inf
                            for key in colors_range.keys():
                                clr_range = colors_range[key]
                                dist = abs(piece_val[0] - clr_range[0]) + abs(piece_val[1] - clr_range[1]) + abs(
                                    piece_val[2] - clr_range[2])
                                if (dist < min_dist):
                                    min_dist = dist
                                    ret_dict_scan[face][h][2 - w] = key[0]

                            list_temp.append(ret_dict_scan[face][h][2 - w])
                            # print('3333333333333333333333333333333333333333333333')
                            print(list_temp)
                    check4=check3

                # ret_dict_scan[faces[check4]]
                if check4<6:
                    face = faces[check4]
                # else:
                #     face='front'
                global current_face
                current_face=face
                # global ret_dict_scan
                # print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                # print(ret_dict_scan)
                global ret_scan
                if check4<6:
                    ret_scan[faces[check4]]=ret_dict_scan[faces[check4]]


                # print(face)
                # print(ret_scan)
                # if pressedKey == ord('n'):
                #     try:
                #         face = next(face_iter)
                #     except:
                #         break
                #
                # if pressedKey == ord('q'):
                #     break

                ret, buffer = cv2.imencode('.jpg', im)
                frame = buffer.tobytes()



            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return ret_dict_scan

@app.route('/calibration')
def generate_frames_calibration():

    colors = ["WHITE", "ORANGE", "RED", "YELLOW", "GREEN", "BLUE"]
    clr_iter = iter(colors)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 2

    cap = cv2.VideoCapture(1)
    ret = True
    clr = next(clr_iter)
    global check1


    if check1 >= len(colors):
        return 'hello'

    else:

        while (ret):

            ## read the camera frame
            ret, im = cap.read()
            if not ret:
                break
            else:
                frame_width = int(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
                frame_height = int(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

                top_left = (int(frame_width / 3), int(frame_height / 3))
                pcs_width = int(0.05 * frame_width)
                gap = pcs_width
                start_pts = [(top_left[0] + (0.5 * gap), top_left[1] + (0.5 * gap))]

                start_loc = (int(start_pts[0][0] + (2 * gap)), int(start_pts[0][1] + (2 * gap)))
                end_loc = (int(start_loc[0] + gap), int(start_loc[1] + gap))

                im = cv2.flip(im, 1)
                im = draw_cube_boundry_calibration(im, frame_width, frame_height)

                im = cv2.putText(im, 'Calibrating cube... Please show ' + clr + ' color :: press c to continue', org,
                                 font,
                                 fontScale, color, 1, cv2.LINE_AA)

                # cv2.imshow('frame', im)

                # pressedKey = cv2.waitKey(1) & 0xFF

                global check2
                # print('check: ', check1, " ", check2)
                if check1 >= check2:
                    ret_dict[clr] = cv2.mean(im[start_loc[1]:start_loc[1] + gap, start_loc[0]:start_loc[0] + gap])[:3]
                    try:
                        clr = colors[check2]

                    except:
                        break
                check2 = check1
                # if pressedKey == ord('q'):
                #     break

                # pressedKey=False

                ret, buffer = cv2.imencode('.jpg', im)
                frame = buffer.tobytes()
                if len(ret_dict) == 6:
                    # save the scanned color ranges to a file
                    with open('colors_range.txt', 'w') as convert_file:
                        convert_file.write(json.dumps(ret_dict))

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def draw_cube_boundry(image, frame_width, frame_height):
    top_left = (int(frame_width / 3)-10, int(frame_height / 3)-10)
    pcs_width = int(0.05 * frame_width)
    gap = pcs_width
    bottom_right = (top_left[0] + 6 * gap+50, top_left[1] + 6 * gap+50)
    color = (255, 0, 0)
    thickness = 2

    cv2.rectangle(image, top_left, bottom_right, color, thickness)

    start_pts = [(top_left[0] + (0.5 * gap)+50, top_left[1] + (0.5 * gap)+50)]
    for h in range(3):
        for w in range(3):
            next_start_w = int(start_pts[0][0] + (gap * w * 2))-20
            next_start_h = int(start_pts[0][1] + (gap * h * 2))-20

            next_end_w = next_start_w + gap-20
            next_end_h = next_start_h + gap-20

            cv2.rectangle(image, (next_start_w, next_start_h), (next_end_w, next_end_h), color, thickness)

    return image


def draw_cube_boundry_calibration(image, frame_width, frame_height):
    top_left = (int(frame_width / 3), int(frame_height / 3))
    pcs_width = int(0.05 * frame_width)
    gap = pcs_width
    color = (255, 0, 0)
    thickness = 2

    start_pts = [(top_left[0] + (0.5 * gap), top_left[1] + (0.5 * gap))]

    next_start_w = int(start_pts[0][0] + (gap * 2))
    next_start_h = int(start_pts[0][1] + (gap * 2))

    next_end_w = next_start_w + gap
    next_end_h = next_start_h + gap

    cv2.rectangle(image, (next_start_w, next_start_h), (next_end_w, next_end_h), color, thickness)

    return image


# colors_range = generate_frames_calibration()
# print('colors range: ')
# print(colors_range)
# print('type: ',type(colors_range))
# cube_name=input('Please enter the cube name to store the scanned color ranges: ')
# file_name=cube_name+".txt"

# save the scanned color ranges to a file
# with open('colors_range.txt', 'w') as convert_file:
#     convert_file.write(json.dumps(colors_range))

# with open('colors_range.txt') as f:
#     data = f.read()
#
# # load the colors
# colors_range_read = json.loads(data)
# # print('color range read: ')
# # print(colors_range_read)
#
# # scanning faces
# utils.cube = generate_frames_scan(colors_range_read)
# print('**********************************************************')
# print(utils.cube)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calibrate')
def calibrate():
    generate_frames_calibration()
    # print('colors range: ')
    # print(colors_range)


    return render_template('colorcalib.html',buttons="""<a href=# id=test_calib><button  type="button" class="btn btn-primary btn-lg btn-danger" style="width: 50%; margin-left: auto;margin-right: auto;"><i class='fas fa-camera'></i> Capture</button></a>""")

@app.route('/background_process_test')
def background_process_test():
    global check3
    check3 = check3 + 1
       # return render_template('cubescan.html',buttons="""<a href="/" ><button  type="button" class="btn btn-primary btn-lg btn-danger" style="width: 50%; margin-left: auto;margin-right: auto;"><i class='fas fa-eye'></i> View Solution</button></a>""")

    with open('colors_range.txt') as f:
        data = f.read()

    # load the colors
    colors_range_read = json.loads(data)
    # global ret_dict_scan
    # print(ret_dict_scan)
    generate_frames_scan(colors_range_read)

    # print("Hello")
    if check3 == 7:
        check3 = 0
        return json.loads('{ "status":"done"}')

    return "nothing"

@app.route('/background_process_test_calib')
def background_process_test_calib():

    global check1

    check1 = check1 + 1

    generate_frames_calibration()

    # print("Hello")
    if check1 == 6:
        check1 = 0
        return json.loads('{ "status":"done"}')

    return "nothing"

@app.route('/scan')
def scan():
    with open('colors_range.txt') as f:
        data = f.read()
    # load the colors
    colors_range_read = json.loads(data)
    generate_frames_scan(colors_range_read)

    # print('faces: ')
    # global ret_dict_scan
    # print(ret_dict_scan)
    # print(type(ret_dict_scan))
    # global final_scan
    # global current_face
    # final_scan[current_face]=ret_dict_scan[current_face]
    # print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
    # print(final_scan)
    # x=ret_dict_scan
    # solution=cube_solution_script.get_rubic_solution(x)
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # print(solution)

    # print('colors range: ')
    # print(colors_range)

    return render_template('cubescan.html',buttons="""<a href=# id=test><button  type="button" class="btn btn-primary btn-lg btn-danger" style="width: 50%; margin-left: auto;margin-right: auto;"><i class='fas fa-camera'></i> Capture</button></a>""")


@app.route('/video_scan')
def video_scan():
    with open('colors_range.txt') as f:
        data = f.read()
    # load the colors
    colors_range_read = json.loads(data)
    # print(colors_range_read)
    return Response(generate_frames_scan(colors_range_read), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_calibration')
def video_calibration():
    return Response(generate_frames_calibration(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/view_solution')
def view_solution():
    global list_temp
    print('')
    print(list_temp)
    #list_temp=['B', 'B', 'B', 'B', 'G', 'B', 'B', 'B', 'B', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'G', 'G', 'G', 'G', 'B', 'G', 'G', 'G', 'G', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'Y', 'Y', 'Y', 'Y', 'W', 'Y', 'Y', 'Y', 'Y', 'W', 'W', 'W', 'W', 'Y', 'W', 'W', 'W', 'W']
    solution_list=list(cube_solution_script.get_rubic_solution(list_temp))

    n = 0
    middle_output = """"""
    final_output = """"""

    while n < len(solution_list):
        if solution_list[n] == 'D':
            if solution_list[n + 1] == ' ':
                n = n + 1
                middle_output = html_string_creation("D.png", "Rotate 90 degrees clockwise")

            elif solution_list[n + 1] == "'":
                n = n + 2
                middle_output = html_string_creation("D'.png", "Rotate 90 degrees anti-clockwise")

            elif solution_list[n + 1] == '2':
                n = n + 2
                middle_output = html_string_creation("D.png", "Rotate 180 degrees")

        elif solution_list[n] == 'L':
            if solution_list[n + 1] == ' ':
                n = n + 1
                middle_output = html_string_creation("L.png", "Rotate 90 degrees")

            elif solution_list[n + 1] == "'":
                n = n + 2
                middle_output = html_string_creation("L'.png", "Rotate 90 anti-degrees")

            elif solution_list[n + 1] == '2':
                n = n + 2
                middle_output = html_string_creation("L.png", "Rotate 180 degrees")

        elif solution_list[n] == 'F':
            if solution_list[n + 1] == ' ':
                n = n + 1
                middle_output = html_string_creation("F.png", "Rotate 90 degrees")

            elif solution_list[n + 1] == "'":
                n = n + 2
                middle_output = html_string_creation("F'.png", "Rotate 90 anti-degrees")

            elif solution_list[n + 1] == '2':
                n = n + 2
                middle_output = html_string_creation("F.png", "Rotate 180 degrees")

        elif solution_list[n] == 'R':
            if solution_list[n + 1] == ' ':
                n = n + 1
                middle_output = html_string_creation("R.png", "Rotate 90 degrees")

            elif solution_list[n + 1] == "'":
                n = n + 2
                middle_output = html_string_creation("R'.png", "Rotate 90 anti-degrees")

            elif solution_list[n + 1] == '2':
                n = n + 2
                middle_output = html_string_creation("R.png", "Rotate 180 degrees")

        elif solution_list[n] == 'U':
            if solution_list[n + 1] == ' ':
                n = n + 1
                middle_output = html_string_creation("U.png", "Rotate 90 degrees")

            elif solution_list[n + 1] == "'":
                n = n + 2
                middle_output = html_string_creation("U'.png", "Rotate 90 anti-degrees")

            elif solution_list[n + 1] == '2':
                n = n + 2
                middle_output = html_string_creation("U.png", "Rotate 180 degrees")

        elif solution_list[n] == 'B':
            if solution_list[n + 1] == ' ':
                n = n + 1
                middle_output = html_string_creation("B.png", "Rotate 90 degrees")

            elif solution_list[n + 1] == "'":
                n = n + 2
                middle_output = html_string_creation("B'.png", "Rotate 90 anti-degrees")

            elif solution_list[n + 1] == '2':
                n = n + 2
                middle_output = html_string_creation("B.png", "Rotate 180 degrees")

        final_output = final_output + middle_output
        n = n + 1
        # print(final_output)
    return render_template('finalResult.html',images=final_output)

if __name__ == "__main__":
    app.run(debug=True)