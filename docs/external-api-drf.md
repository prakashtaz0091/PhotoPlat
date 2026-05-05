## 🧩 1. Problem Statement

“We already built a Django app where users can browse and book photographers.

Now imagine another company comes to us and says:

> ‘We want to use your photographer network inside our app.’

So the question is:
👉 *How do two different systems talk to each other?*

Answer: **APIs**

And for Django, we use:
👉 Django REST Framework”

---

## 🧩 2. The API (Before Writing Code)

“Before writing any code, we must define what our API looks like.

Let’s design one endpoint:

```http
GET /api/photographers/
```

And it should return something like:

```json
[
  {
    "id": 1,
    "name": "Ram",
    "city": "Kathmandu",
    "verified": true
  }
]
```

👉 This is called an **API contract**.
Clients depend on this, so we don’t randomly change it later.”

---

## 🧩 3. Existing Model

“We already have data in our database. For example:”

```python
     
class Profile(models.Model):
    
    class EMAIL_STATUS(models.TextChoices):
        PENDING = ("pending", "Pending")
        VERIFIED = ("verified", "Verified")
        
    class KYC_STATUS(models.TextChoices):
        NOT_SUBMITTED = ("not_submitted", "Not Submitted")
        IN_REVIEW = ("in_review", "In Review")
        REJECTED = ("rejected", "Rejected")
        VERIFIED = ("verified", "Verified")
    
    
    class CURRENCY_CHOICES(models.TextChoices):
        NPR = ('npr', 'रु')
        INR = ('inr', '₹')
        USD = ('usd', '$')
    

    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=60, null=True, verbose_name=_("Full Name"))
    date_of_birth = models.DateField(null=True, verbose_name=_("Date of birth"))
    citizenship_no = models.CharField(max_length=20, null=True, verbose_name=_("Citizenship No")) # xx-xx-xx-xxxxx
    issued_district = models.CharField(max_length=30, null=True, verbose_name=_("Issued District"))
    permanent_address = models.CharField(max_length=100, null=True, verbose_name=_("Permanent Address"))
    specialities = models.ManyToManyField(Speciality, related_name="profiles", verbose_name=_("Specialities"))
    
    # documents
    profile_photo = models.ImageField(upload_to="profile_photos", null=True, blank=True, validators=[validate_file_size], verbose_name=_("Profile Photo"))
    citizenship_front = models.ImageField(upload_to="citizenships", null=True, blank=True, validators=[validate_file_size], verbose_name=_("Citizenship Front"))
    citizenship_back = models.ImageField(upload_to="citizenships", null=True, blank=True, validators=[validate_file_size], verbose_name=_("Citizenship Back"))
    
    # verification
    email_verified = models.CharField(choices=EMAIL_STATUS, default=EMAIL_STATUS.PENDING, verbose_name=_("Email Verification Status"))
    kyc_verified = models.CharField(choices=KYC_STATUS, default=KYC_STATUS.NOT_SUBMITTED, verbose_name=_("KYC Verification Status"))
    
    # rejection reason
    rejection_reason = models.TextField(null=True, blank=True, verbose_name=_("Rejection Reason"))
    
    # pricing
    currency = models.CharField(choices=CURRENCY_CHOICES, default="npr", verbose_name=_("Currency"))
    per_day_fee = models.PositiveIntegerField(default=0, verbose_name=_("Per day fee")) 
    
    def __str__(self):
        return f"{self.user.email}'s profile"

```

“So we are not creating new data—we are just exposing it.”

---

## 🧩 4. The Serializer

“To convert this model into JSON, we use a serializer.”

```python
from rest_framework.serializers import ModelSerializer

class PhotographerSerializer(ModelSerializer):
    class Meta:
        model = Photographer
        fields = ["id", "name", "city", "is_verified"]
```

👉 “Serializer = Model → JSON”

---

## 🧩 5.  First API

“Now let’s create our first API.”

```python
from rest_framework.generics import ListAPIView

class PhotographerListAPI(ListAPIView):
    queryset = Photographer.objects.filter(is_verified=True)
    serializer_class = PhotographerSerializer
```

👉 “Notice:
We are only exposing **verified photographers**.”

---

## 🧩 6. Connecting URL

```python
urlpatterns = [
    path("api/photographers/", PhotographerListAPI.as_view()),
]
```

---

## 🧪 7. Testing the API

“Let’s test this in browser/Postman.”

👉 Show response

“Now we have a working API 🎉”

---

# 🔐 8. Security Problem

“Now think about this:

👉 Right now, *anyone* can access our API.

But in real life:

* This is our business
* We don’t want to give it for free

So we need:
👉 **Authentication for external apps**”

---

## 🧩 9. API Key Concept

“We’ll give each client an API key.

They must send it with every request.”

---

### Model:

```python
class APIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
```

---

## 🧩 10. Custom Authentication

“Now we teach DRF how to check API keys.”

```python
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get("Authorization")

        if not key:
            raise AuthenticationFailed("API key required")

        try:
            api_key = APIKey.objects.get(key=key, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        return (api_key, None)
```

👉 “This runs on every request.”

---

## 🧩 11. Attach Authentication

```python
class PhotographerListAPI(ListAPIView):
    queryset = Photographer.objects.filter(is_verified=True)
    serializer_class = PhotographerSerializer
    authentication_classes = [APIKeyAuthentication]
```

---

## 🧪 12. Test with API Key

“Now test again.”

Without key → ❌ error
With key:

```bash
curl -H "Authorization: abc123" \
http://localhost:8000/api/photographers/
```

👉 “Now it works ✅”

---

# 🧩 13. Real Use Case – Booking API

“Let’s make it more real.

Clients don’t just want to *view* photographers.
They want to **book them**.”

---

### Endpoint:

```http
POST /api/bookings/
```

---

### Serializer:

```python
class BookingSerializer(serializers.Serializer):
    photographer_id = serializers.IntegerField()
    event_date = serializers.DateField()
```

---

### API:

```python
from rest_framework.views import APIView

class BookingAPI(APIView):
    authentication_classes = [APIKeyAuthentication]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message": "Booking created"})
```

👉 “Now we support **write operations**.”

---

# 🧩 14. Add Pagination

“What if we have 10,000 photographers?”

👉 “We don’t send all at once.”

```python
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 2
```

Attach it:

```python
class PhotographerListAPI(ListAPIView):
    pagination_class = CustomPagination
```

👉 Test:

```
/api/photographers/?page=2
```

---

# 🧩 15. Add Filtering

“What if client only wants photographers from Kathmandu?”

```python
def get_queryset(self):
    city = self.request.query_params.get("city")
    qs = Photographer.objects.filter(is_verified=True)

    if city:
        qs = qs.filter(city=city)

    return qs
```

👉 Test:

```
/api/photographers/?city=Kathmandu
```

---

# 🧠 16. Connect Everything

“Let’s recap what we built:

* Serializer → converts data
* View → handles request
* API → exposes data
* API Key → secures access
* Pagination → handles large data
* Filtering → flexible queries”

---

# ⚠️ 17. Important Notes

“Remember:

* API is not UI
* API is for systems to communicate
* Security is not optional
* Good design matters more than code”

---

# ❓ 18. End with Questions

“Think about this:

1. Should API keys expire?
2. Should we limit requests per client?
3. What if someone abuses our API?
4. Should different clients get different data?”
