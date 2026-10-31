raw_services = [
    {"service_code": "S301", "department": "cardiology", "price": 650000, "status": "active"},
    {"service_code": " s101", "department": "pediatrics", "price": 250000, "status": "active"},
    {"service_code": "S202", "department": "dermatology", "price": 400000, "status": "paused"},
    {"service_code": "S102", "department": "pediatrics", "price": 300000, "status": "inactive"},
    {"service_code": "S302", "department": "cardiology", "price": 800000, "status": "active"},
]


def clean_and_validate_services(services):
    clean_services = []

    for service in services:
        service_code = service["service_code"].strip().upper()

        if service_code.startswith("S") and service_code[1:].isdigit():
            new_service = service.copy()
            new_service["service_code"] = service_code
            clean_services.append(new_service)

    return clean_services


def search_services(services, max_price, status=None):
    result = []

    for service in services:
        if service["price"] <= max_price:
            if status is None or service["status"] == status:
                result.append(service)

    return result


def sort_services_by_price_desc(services):
    result = services.copy()
    n = len(result)

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            if result[j]["price"] < result[j + 1]["price"]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result


clean_services = clean_and_validate_services(raw_services)

print("1. DANH SÁCH SAU KHI CHUẨN HÓA:")
for service in clean_services:
    print(service)

print("\n2. KẾT QUẢ TÌM KIẾM:")
search_result = search_services(clean_services, 400000, "active")

for service in search_result:
    print(service)

print("\n3. KẾT QUẢ SẮP XẾP GIẢM DẦN:")
sorted_services = sort_services_by_price_desc(clean_services)

for service in sorted_services:
    print(service)