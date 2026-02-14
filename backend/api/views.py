# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .ml_model import predict_disease
# from .mongo import drug_collection, history_collection
# import datetime

# @api_view(['POST'])
# def predict(request):
#     symptoms = request.data.get("symptoms")

#     disease, probability = predict_disease(symptoms)

#     drug_data = drug_collection.find_one({"disease": disease}, {"_id": 0})
#     medicines = drug_data["medicines"] if drug_data else []

#     history_collection.insert_one({
#         "symptoms": symptoms,
#         "disease": disease,
#         "probability": probability,
#         "date": datetime.datetime.now()
#     })

#     response = {
#         "disease": disease,
#         "probability": f"{probability}%",
#         "medicines": []
#     }

#     for med in medicines:
#         response["medicines"].append({
#             "name": med,
#             "amazon": f"https://www.amazon.in/s?k={med}",
#             "flipkart": f"https://www.flipkart.com/search?q={med}"
#         })

#     return Response(response)

# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# @api_view(['POST'])
# def register(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     if User.objects.filter(username=username).exists():
#         return Response({"error": "User already exists"})

#     User.objects.create_user(username=username, password=password)
#     return Response({"message": "User registered successfully"})


# @api_view(['POST'])
# def login_user(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(username=username, password=password)
#     if user:
#         return Response({"message": "Login successful"})
#     return Response({"error": "Invalid credentials"})



# @api_view(['GET'])
# def get_history(request):
#     records = history_collection.find({}, {"_id": 0})
#     return Response(list(records))


# from reportlab.pdfgen import canvas
# from django.http import HttpResponse
# import io

# @api_view(['GET'])
# def generate_report(request):
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer)

#     p.drawString(100, 800, "Medical Prediction Report")
#     p.drawString(100, 770, "--------------------------------")

#     y = 740
#     records = history_collection.find({}, {"_id": 0})

#     for r in records:
#         p.drawString(100, y, f"Disease: {r['disease']} | Probability: {r['probability']}%")
#         y -= 20

#     p.showPage()
#     p.save()

#     buffer.seek(0)
#     return HttpResponse(buffer, content_type='application/pdf')






from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ml_model import predict_disease
from .mongo import drug_collection, history_collection
import datetime


# ==============================
# 🔮 DISEASE PREDICTION API
# ==============================
@api_view(['POST'])
def predict(request):
    symptoms = request.data.get("symptoms")

    if not symptoms:
        return Response({"error": "No symptoms provided"}, status=400)

    disease, probability = predict_disease(symptoms)

    # Get medicines from MongoDB
    drug_data = drug_collection.find_one({"disease": disease}, {"_id": 0})
    medicines = drug_data["medicines"] if drug_data else []

    # If no DB medicines → auto-generate
    if not medicines:
        medicines = [
            f"{disease} Relief Tablet",
            f"{disease} Care Syrup",
            f"{disease} Support Capsule"
        ]

    # Save history
    history_collection.insert_one({
        "symptoms": symptoms,
        "disease": disease,
        "probability": probability,
        "date": datetime.datetime.now()
    })

    response = {
        "disease": disease,
        "probability": probability,
        "medicines": []
    }

    for med in medicines:
        response["medicines"].append({
            "name": med,
            "amazon": f"https://www.amazon.in/s?k={med}",
            "flipkart": f"https://www.flipkart.com/search?q={med}",
            "blinkit": f"https://blinkit.com/s/?q={med}",
            "bigbasket": f"https://www.bigbasket.com/ps/?q={med}",
            "apollo": f"https://www.apollopharmacy.in/search-medicines/{med}",
            "tata1mg": f"https://www.1mg.com/search/all?name={med}",
            "netmeds": f"https://www.netmeds.com/catalogsearch/result?q={med}"
        })

    return Response(response)



# ==============================
# 👤 REGISTER
# ==============================
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"})

    User.objects.create_user(username=username, password=password)
    return Response({"message": "User registered successfully"})


# ==============================
# 🔐 LOGIN
# ==============================
@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        return Response({"message": "Login successful"})
    return Response({"error": "Invalid credentials"})


# ==============================
# 📜 HISTORY
# ==============================
@api_view(['GET'])
def get_history(request):
    records = history_collection.find({}, {"_id": 0})
    return Response(list(records))


# ==============================
# 📄 PDF REPORT
# ==============================
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import io

@api_view(['GET'])
def generate_report(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, "Medical Prediction Report")
    p.drawString(100, 770, "--------------------------------")

    y = 740
    records = history_collection.find({}, {"_id": 0})

    for r in records:
        p.drawString(
            100,
            y,
            f"Disease: {r['disease']} | Probability: {r['probability']}%"
        )
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

