import streamlit as st
import pandas as pd
import os
import datetime

st.set_page_config(layout="wide")

st.title("📚 Sách Giáo Dục Mầm Non")

# Đọc Excel
df = pd.read_excel("data/products.xlsx")

# Giỏ hàng
if "cart" not in st.session_state:
    st.session_state.cart = {}

st.subheader("Danh sách sách")

cols = st.columns(3)

for index, row in df.iterrows():
    img_path = os.path.basename(row["image"])
    with cols[index % 3]:
        st.image(f"images/{img_path}", use_column_width=True)
        st.write(f"### {row['name']}")
        st.write(f"Giá: {row['price']:,} VNĐ")

        qty = st.number_input(
            f"Số lượng {row['id']}",
            min_value=1,
            value=1,
            key=f"qty_{row['id']}"
        )

        if st.button(f"Thêm vào giỏ {row['id']}"):
            pid = str(row["id"])
            if pid in st.session_state.cart:
                st.session_state.cart[pid]["quantity"] += qty
            else:
                st.session_state.cart[pid] = {
                    "name": row["name"],
                    "price": row["price"],
                    "quantity": qty
                }

# ===== GIỎ HÀNG =====
st.sidebar.title("🧺 Giỏ hàng")

total = 0
for item in st.session_state.cart.values():
    item_total = item["price"] * item["quantity"]
    total += item_total
    st.sidebar.write(
        f"{item['name']} x {item['quantity']} = {item_total:,} VNĐ"
    )

st.sidebar.markdown("---")
st.sidebar.subheader(f"Tổng tiền: {total:,} VNĐ")

# ===== THANH TOÁN =====
st.sidebar.markdown("## 💳 Thanh toán")

payment_method = st.sidebar.radio(
    "Chọn phương thức:",
    ["Quét QR", "Thẻ ngân hàng"]
)

if payment_method == "Quét QR":
    st.sidebar.image("images/qr.png", caption="Quét mã để thanh toán")

else:
    st.sidebar.text_input("Số thẻ")
    st.sidebar.text_input("Tên chủ thẻ")
    st.sidebar.text_input("Ngày hết hạn")
    st.sidebar.button("Thanh toán")


st.sidebar.markdown("## 📝 Thông tin khách hàng")

customer_name = st.sidebar.text_input("Tên khách hàng")
phone = st.sidebar.text_input("Số điện thoại")
address = st.sidebar.text_input("Địa chỉ")

if st.sidebar.button("✅ Xác nhận thanh toán"):
    if len(st.session_state.cart) == 0:
        st.sidebar.warning("Giỏ hàng trống!")
    else:
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        order_data = []

        for item in st.session_state.cart.values():
            order_data.append({
               "time": order_time,
               "customer": customer_name,
               "phone": phone,
               "address": address,
               "product": item["name"],
               "quantity": item["quantity"],
               "price": item["price"],
               "total": item["price"] * item["quantity"],
               "checked": False   # <- thêm dòng này
            })

        order_df = pd.DataFrame(order_data)

        # Nếu file đã tồn tại thì ghi tiếp
        if os.path.exists("orders.xlsx"):
            old_df = pd.read_excel("orders.xlsx")
            order_df = pd.concat([old_df, order_df], ignore_index=True)

        order_df.to_excel("orders.xlsx", index=False)

        st.sidebar.success("🎉 Đặt hàng thành công! Shop sẽ liên hệ bạn.")
        st.session_state.cart = {}
