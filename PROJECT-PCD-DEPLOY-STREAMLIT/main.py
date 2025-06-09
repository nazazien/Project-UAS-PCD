from keperluan_modul import *

UPLOAD_DIR = "uploaded_images"
CSV_PATH = "Documents/user_data.csv"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def preprocess_image(image_array, use_grayscale=False):
    image = image_array.copy()
    
    if use_grayscale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    # Pastikan tipe data uint8
    if image.dtype != np.uint8:
        image = np.clip(image, 0, 255).astype(np.uint8)
    
    return image

def embed_message_lsb(image, message):
    message += "#"
    message_bits = ''.join(format(ord(c), '08b') for c in message)
    rows, cols, channels = image.shape
    max_bits = rows * cols * channels

    if len(message_bits) > max_bits:
        raise ValueError("Pesan terlalu panjang untuk disisipkan dalam gambar!")

    stego_image = image.copy()
    bit_idx = 0
    for row in range(rows):
        for col in range(cols):
            for ch in range(channels):
                if bit_idx < len(message_bits):
                    pixel_val = stego_image[row, col, ch]
                    pixel_val = (pixel_val & 0b11111110) | int(message_bits[bit_idx])
                    stego_image[row, col, ch] = pixel_val
                    bit_idx += 1
                else:
                    break
    return stego_image

def extract_message_lsb(stego_image_path):
    stego_image = cv2.imread(stego_image_path)
    if stego_image is None:
        raise ValueError("Gambar tidak ditemukan!")

    rows, cols, channels = stego_image.shape
    message_bits = ""
    for row in range(rows):
        for col in range(cols):
            for ch in range(channels):
                message_bits += str(stego_image[row, col, ch] & 1)

    chars = [chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8)]
    extracted_message = ''.join(chars)
    if "#" in extracted_message:
        extracted_message = extracted_message[:extracted_message.index("#")]

    return extracted_message

def calculate_psnr(original, stego):
    mse = np.mean((original.astype(np.float32) - stego.astype(np.float32)) ** 2)
    if mse == 0:
        return 100.0
    PIXEL_MAX = 255.0
    psnr = 10 * np.log10((PIXEL_MAX ** 2) / mse)
    return psnr

def get_psnr_category(psnr):
    if psnr < 20:
        return "☹️ Kualitas Citra Rendah"
    elif 20 <= psnr < 30:
        return "😑 Kualitas Citra Cukup Baik"
    elif 30 <= psnr < 40:
        return "☺️ Kualitas Citra Baik"
    else:
        return "🤩 Kualitas Citra Luar Biasa"

def load_csv_data():
    data = {}
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    psnr_value = float(row["psnr"])
                except ValueError:
                    psnr_value = None 

                data[row["file_url"]] = {
                    "pesan": row["pesan"],
                    "psnr": psnr_value,
                    "timestamp": row["timestamp"]
                }
    return data

@st.dialog("📦 Pesan Ditemukan")
def show_extracted_message(pesan, psnr=None, kategori=None, timestamp=None):    
    if timestamp:
        st.markdown(
            f"<div style='text-align: right; color: grey; font-size: 12px;'>{timestamp}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='text-align: right; color: grey; font-size: 12px;'>Tidak tersedia</div>",
            unsafe_allow_html=True
        )
   
    st.write("### 💬 ",pesan)
    st.subheader("")
    
    if psnr:
        st.markdown(
            f"<div style='font-size: 13px;'><b>PSNR</b>: {psnr:.2f} dB — <b>{kategori}</b></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='font-size: 13px;'><i>PSNR tidak tersedia</i></div>",
            unsafe_allow_html=True
        )

def show_gallery():
    st.header(':rainbow[GALERI]', divider='rainbow')
    images = os.listdir(UPLOAD_DIR)
    images = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        st.info("Belum ada gambar yang diupload.")
        return

    csv_data = load_csv_data()

    cols_per_row = 4
    rows = ceil(len(images) / cols_per_row)
    for row in range(rows):
        cols = st.columns(cols_per_row)
        for i in range(cols_per_row):
            idx = row * cols_per_row + i
            if idx < len(images):
                img_name = images[idx]
                img_path = os.path.join(UPLOAD_DIR, img_name)
                img = Image.open(img_path)
                img = ImageOps.pad(img, (300, 300), method=Image.Resampling.LANCZOS, color=(255,255,255))
                cols[i].image(img)

                col_hapus, col_ekstrak = cols[i].columns([2,1])

                if col_hapus.button("Hapus", key=f"hapus_{img_name}"):
                    os.remove(img_path)
                    st.rerun()

                if col_ekstrak.button("Ekstrak", key=f"ekstrak_{img_name}"):
                    try:
                        extracted_message = extract_message_lsb(img_path)                        
                        info = csv_data.get(img_path, None)
                        if info:
                            psnr = info["psnr"]
                            timestamp = info["timestamp"]
                            kategori = get_psnr_category(psnr)
                        else:
                            psnr = None
                            timestamp = "Tidak tersedia"
                            kategori = "Tidak tersedia"

                        show_extracted_message(
                            pesan=extracted_message,
                            psnr=psnr,
                            kategori=kategori,
                            timestamp=timestamp
                        )

                    except Exception as e:
                        st.error(f"Gagal mengekstrak pesan: {e}")


def main():
    bg()
    st.image(Image.open('Documents/image/bb.png'))
    st.write('')
    st.header(':rainbow[AYO COBA STEGANOGRAFI FOTO ANDA!]', divider='rainbow')
    st.write(':grey[Friday, 14 Mei 2025. By [gemilang.com](http://localhost:8501/%F0%9F%91%A5%20About%20Us)]')
    st.subheader("")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Upload atau Ambil Gambar")
        camera_image = st.camera_input("Ambil gambar dari kamera")
        uploaded_file = st.file_uploader("Upload gambar dari file", type=["png", "jpg", "jpeg"])

        image_array = None
        image_name = None

        if camera_image:
            image_name = f"camera_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            image = Image.open(camera_image)
            image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        elif uploaded_file:
            image_name = uploaded_file.name
            image = Image.open(uploaded_file)
            image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    with col2:
        st.write("Tulis Pesan")
        text_message = st.text_area("Pesan Teks", height=200)
        if st.button("Simpan Pesan"):
            if not text_message:
                st.error("Pesan tidak boleh kosong!")
            elif image_array is None:
                st.error("Gambar belum dipilih atau diambil!")
            else:
                try:
                    pemanis.sukses()
                    preprocessed_img = preprocess_image(image_array)
                    stego_image = embed_message_lsb(preprocessed_img, text_message)

                    base_name, ext = os.path.splitext(image_name)
                    stego_filename = f"{base_name}_stego.png"
                    stego_path = os.path.join(UPLOAD_DIR, stego_filename)

                    cv2.imwrite(stego_path, stego_image)

                    psnr = calculate_psnr(preprocessed_img, stego_image)

                    
                    if not os.path.exists(CSV_PATH):
                        with open(CSV_PATH, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(["id", "file_url", "pesan", "psnr", "timestamp"])

                    new_id = str(int(time.time()))
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(CSV_PATH, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([new_id, stego_path, text_message, psnr, timestamp])
                    st.success(f"Gambar dan pesan berhasil disisipkan dan disimpan!\nPSNR: {psnr:.2f} dB")                    

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menyisipkan pesan: {e}")

    st.subheader("")
    show_gallery()
    st.subheader("")

    st.header(':rainbow[ABOUT US]', divider='rainbow')
    st.subheader('We are behind the scenes of Gemilang!')    

    col1,col2,col3 = st.columns([2,2,2])
    with col1:
        st.image(Image.open('Documents/image/naza.jpg'), width=150)
        st.markdown('''Naza Sulthoniyah Wahda
                    23031554026
                    naza.23026@gmail.com''')

    with col2:
        st.image(Image.open('Documents/image/salwa.jpeg'), width=150)
        st.markdown('''Salwa Nadhifah Az Zahrah
                    23031554136
                    salwa.23136@mhs.unesa.ac.id''')

    with col3:
        st.image(Image.open('Documents/image/salsa.jpg'), width=150)
        st.markdown('''Salsabilla Indah Rahmawati
                    23031554193
                    salsabilla.23193@mhs.unesa.ac.id''')


    

if __name__ == "__main__":
    main()
