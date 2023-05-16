# coding: utf-8

import re
import io
import os
from google.cloud import vision
import fitz
from PIL import Image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/lixingying/Desktop/flask_pdf_to_str/i-mariner-383504-3b9b518dc2c6.json'  # credenticals


# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'c:/i-mariner-383504-3b9b518dc2c6.json'  # credenticals

def detect_text_v2(img_path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image, )

    blocks = response.text_annotations
    # blocks_sorted = sorted(blocks, key=lambda b: (b.bounding_poly.vertices[0].y, b.bounding_poly.vertices[0].x))

    # print text in order
    s = ""
    for block in blocks:
        print(block.description)
        s += block.description + " "
    print("0" * 20, s)
    return s

#image positioning
def pdf2png(pdf_file_path, save_file_path):
    """
    pdf to save imgs
    :param pdf_file_path:
    :param save_file_path:
    :return:
    """
    pdf_file = fitz.Document(pdf_file_path)

    for p, page in enumerate(pdf_file.pages(), 1):
        pix = page.get_pixmap()
        new_save_file_path = f"{save_file_path}{pdf_file_path[-5::]}_{p}.png"
        pix.save(new_save_file_path)  # save whole image
        new_save_path = crop(new_save_file_path)  # Save the picture after cutting and return to the new address
        print(new_save_path)
        yield new_save_path
        # parse each pdf content
    pdf_file.close()
    return

# image cutting
def crop(file_path):
    # Open the input image file
    new_save_path = []
    with Image.open(file_path) as im:
        # Crop the image to the specified box coordinates
        # box = (26, 220, 620, 350)  # the whole interface
        box = (120, 120, 600, 210)  # 1
        cropped_im = im.crop(box)
        new_save_path1 = f"{file_path}_crop1.png"
        cropped_im.save(new_save_path1)
        #
        box = (20, 215, 600, 285)  # 2
        cropped_im = im.crop(box)
        new_save_path2 = f"{file_path}_crop2.png"
        cropped_im.save(new_save_path2)
        #
        box = (20, 285, 600, 340)  # 3
        cropped_im = im.crop(box)
        new_save_path3 = f"{file_path}_crop3.png"
        cropped_im.save(new_save_path3)
        new_save_path = [new_save_path1, new_save_path2, new_save_path3]
        # new_save_path = [ new_save_path3]
        return new_save_path

# create regular expression to extract text
phone_re = re.compile(r'(\d{2,4}-\d\d\d-\d\d\d\d)')
phone_re1 = re.compile(r'(\d\d\d-\d\d\d\d)')
zip_re = re.compile(r'(\d{5})')
state_re = re.compile(r'State:(.+?)(Zip|\n)')
state_re1 = re.compile(r'State :(.+?)(Zip|\n)')
city_re = re.compile(r'City:(.+?)(\n|Sta|City:|Authorized|Phone)')
city_re1 = re.compile(r'City :(.+?)(\n|Sta|City:|Authorized|Phone)')
generator_name_re = re.compile(r'GENERATOR:.+Name:(.+?)(\n|DEC)')
generator_name_re1 = re.compile(r'GENERATOR:.+Name :(.+?)(\n|DEC)')
of_generator_re = re.compile(r'Authorized.+Representative.+of.+Generator:(.+?)(\n)')
of_generator_re1 = re.compile(r'Authorized.+Representative.+of.+Generator :(.+?)(\n)')
address_re = re.compile(r'Address:(.+?)(\n|City)')
address_re1 = re.compile(r'Address :(.+?)(\n|City)')
transporter_name_re = re.compile(r'Transporter Name:(.+?)(\n)')
transporter_name_re1 = re.compile(r'Transporter Name :(.+?)(\n)')
facility_name_re = re.compile(r'Receiving Facility Name:(.+?)(\n)')
facility_name_re1 = re.compile(r'Receiving Facility Name :(.+?)(\n)')
reg_no_re = re.compile(r'No\. \(if applicable\):(.+?)(\n)')
reg_no_re1 = re.compile(r'No\. \(if applicable\) :(.+?)(\n)')
source_name_re = re.compile(r'Source Name:(.+?)(\n)')


def find_all_fields_v3(s: str):
    res = {"phone": "", "zip": "", "u_zip": "", "state": "", "city": "", "address": "",
           "facility_name": "", "generator_name": "", "of_generator": "", "transporter_name": "",
           "reg_no": "", "source_name": ""}
    source_name_re_ = source_name_re.findall(s)
    if source_name_re_:
        res["source_name"] = source_name_re_[0][0]
    phone_ = phone_re.findall(s)
    if phone_:
        res["phone"] = phone_[0]
    else:
        phone_ = phone_re1.findall(s)
        if phone_:
            res["phone"] = phone_[0]

    zip_re_ = zip_re.findall(s)
    if zip_re_:
        res["zip"] = zip_re_[0]
    if len(zip_re_) > 1:
        res['u_zip'] = zip_re_[-1]

    state_re_ = state_re.findall(s)
    if state_re_:
        res["state"] = state_re_[0][0]
    else:
        state_re_ = state_re1.findall(s)
        if state_re_:
            res["state"] = state_re_[0][0]
    city_re_ = city_re.findall(s)
    if city_re_:
        res["city"] = city_re_[0][0]
    else:
        city_re_ = city_re1.findall(s)
        if city_re_:
            res["city"] = city_re_[0][0]

    generator_name_re_ = generator_name_re.findall(s)
    if generator_name_re_:
        res["generator_name"] = generator_name_re_[0][0]
    else:
        generator_name_re_ = generator_name_re1.findall(s)
        if generator_name_re_:
            res["generator_name"] = generator_name_re_[0][0]
    of_generator_re_ = of_generator_re.findall(s)
    if of_generator_re_:
        res["of_generator"] = of_generator_re_[0][0]
    else:
        of_generator_re_ = of_generator_re1.findall(s)
        if of_generator_re_:
            res["of_generator"] = of_generator_re_[0][0]

    address_re_ = address_re.findall(s)
    if address_re_:
        res["address"] = address_re_[0][0]
    else:
        address_re_ = address_re1.findall(s)
        if address_re_:
            res["address"] = address_re_[0][0]
    transporter_name_re_ = transporter_name_re.findall(s)
    if transporter_name_re_:
        res["transporter_name"] = transporter_name_re_[0][0]
    else:
        transporter_name_re_ = transporter_name_re1.findall(s)
        if transporter_name_re_:
            res["transporter_name"] = transporter_name_re_[0][0]

    facility_name_re_ = facility_name_re.findall(s)
    if facility_name_re_:
        res["facility_name"] = facility_name_re_[0][0]
    else:
        facility_name_re_ = facility_name_re1.findall(s)
        if facility_name_re_:
            res["facility_name"] = facility_name_re_[0][0]

    reg_no_re_ = reg_no_re.findall(s)
    if reg_no_re_:
        res["reg_no"] = reg_no_re_[0][0]
    else:
        reg_no_re_ = reg_no_re1.findall(s)
        if reg_no_re_:
            res["reg_no"] = reg_no_re_[0][0]
    return res


def handler_pdf(save_path, img_path):
    n = 0
    res = {"phone": "", "zip": "", "u_zip": "", "state": "", "city": "", "address": "",
           "facility_name": "", "generator_name": "", "of_generator": "", "transporter_name": "",
           "reg_no": "", "source_name": ""}
    datas = []
    for img_file_path in pdf2png(save_path, img_path):
        data = {"source_name": "", "location_address": "", "location_city": "", "location_state": "",
                "location_zip_code": "",

                "generator_name": "", "reg_no": "", "generator_address": "", "generator_city": "",
                "generator_state": "",
                "generator_zip": "", "generator_of_generator": "", "generator_phone": "",

                "transporter_name": "", "facility_name": "", "state": "", "city": "", "address": "", "zip": "", }
        for img_file in img_file_path:
            n += 1
            print(img_file)
            # s = detect_document(img_file_path)
            # s = detect_text(img_file_path)
            s = detect_text_v2(img_file)
            # # find_all_fields_v2(s)
            res = find_all_fields_v3(s)
            print('\n')
            # print(s)
            print(str(n) * 100)
            print(res)
            if n == 1:
                data["source_name"] = res.get("source_name")
                data["location_address"] = res.get("address")
                data["location_city"] = res.get("city")
                data["location_state"] = res.get("state")
                data["location_zip_code"] = res.get("zip")
            elif n == 2:
                data["generator_name"] = res.get("generator_name")
                data["reg_no"] = res.get("reg_no")
                data["generator_address"] = res.get("address")
                data["generator_city"] = res.get("city")
                data["generator_state"] = res.get("state")
                data["generator_of_generator"] = res.get("generator_name")
                data["generator_phone"] = res.get("phone")
                data["generator_zip"] = res.get("zip")
            elif n == 3:
                data["transporter_name"] = res.get("transporter_name")
                data["facility_name"] = res.get("facility_name")
                data["address"] = res.get("address")
                data["city"] = res.get("city")
                data["state"] = res.get("state")
                data["zip"] = res.get("zip")
        datas.append(data)
        print("=" * 100)
    print("9999:", datas)
    return datas


if __name__ == "__main__":
    save_path, img_path = "test_pdf/1A-371_Asbestos_Trans_cdd.2019-01J.wtd.pdf", "test_pdf/demo.png"
    handler_pdf(save_path, img_path)
    # for img_file_path in pdf2png(save_path, img_path):
    #     print(img_file_path)
    # s = detect_document(img_file_path)
    # s = detect_text(img_file_path)
    # match_txt(s)
    # print("===="*50)
    # find_all_fields_v2(s)
