document.addEventListener("DOMContentLoaded", function () {
    const symptomsList = [
        "Itching", "Skin Rash", "Nodal Skin Eruptions", "Continuous Sneezing", "Shivering", "Chills",
        "Joint Pain", "Stomach Pain", "Acidity", "Ulcers On Tongue", "Muscle Wasting", "Vomiting",
        "Burning Micturition", "Spotting Urination", "Fatigue", "Weight Gain", "Anxiety", "Cold Hands And Feets",
        "Mood Swings", "Weight Loss", "Restlessness", "Lethargy", "Patches In Throat", "Irregular Sugar Level",
        "Cough", "High Fever", "Sunken Eyes", "Breathlessness", "Sweating", "Dehydration", "Indigestion",
        "Headache", "Yellowish Skin", "Dark Urine", "Nausea", "Loss Of Appetite", "Pain Behind The Eyes",
        "Back Pain", "Constipation", "Abdominal Pain", "Diarrhoea", "Mild Fever", "Yellow Urine", "Yellowing Of Eyes",
        "Acute Liver Failure", "Fluid Overload", "Swelling Of Stomach", "Swelled Lymph Nodes", "Malaise",
        "Blurred And Distorted Vision", "Phlegm", "Throat Irritation", "Redness Of Eyes", "Sinus Pressure",
        "Runny Nose", "Congestion", "Chest Pain", "Weakness In Limbs", "Fast Heart Rate",
        "Pain During Bowel Movements", "Pain In Anal Region", "Bloody Stool", "Irritation In Anus",
        "Neck Pain", "Dizziness", "Cramps", "Bruising", "Obesity", "Swollen Legs", "Swollen Blood Vessels",
        "Puffy Face And Eyes", "Enlarged Thyroid", "Brittle Nails", "Swollen Extremities", "Excessive Hunger",
        "Extra Marital Contacts", "Drying And Tingling Lips", "Slurred Speech", "Knee Pain", "Hip Joint Pain",
        "Muscle Weakness", "Stiff Neck", "Swelling Joints", "Movement Stiffness", "Spinning Movements",
        "Loss Of Balance", "Unsteadiness", "Weakness Of One Body Side", "Loss Of Smell", "Bladder Discomfort",
        "Foul Smell Of Urine", "Continuous Feel Of Urine", "Passage Of Gases", "Internal Itching",
        "Toxic Look (Typhos)", "Depression", "Irritability", "Muscle Pain", "Altered Sensorium",
        "Red Spots Over Body", "Belly Pain", "Abnormal Menstruation", "Dischromic Patches",
        "Watering From Eyes", "Increased Appetite", "Polyuria", "Family History", "Mucoid Sputum",
        "Rusty Sputum", "Lack Of Concentration", "Visual Disturbances", "Receiving Blood Transfusion",
        "Receiving Unsterile Injections", "Coma", "Stomach Bleeding", "Distention Of Abdomen",
        "History Of Alcohol Consumption", "Fluid Overload", "Blood In Sputum", "Prominent Veins On Calf",
        "Palpitations", "Painful Walking", "Pus Filled Pimples", "Blackheads", "Scurring",
        "Skin Peeling", "Silver Like Dusting", "Small Dents In Nails", "Inflammatory Nails",
        "Blister", "Red Sore Around Nose", "Yellow Crust Ooze"
    ];

    const symptomInput = document.getElementById("symptoms");
    const suggestionsBox = document.getElementById("suggestions-box");
    let selectedIndex = -1;
    let filteredSymptoms = [];

    // Update suggestions dropdown
    function updateSuggestions() {
        const query = symptomInput.value.trim().toLowerCase();
        suggestionsBox.innerHTML = "";

        if (query.length === 0) return;

        filteredSymptoms = symptomsList.filter(symptom =>
            symptom.toLowerCase().includes(query)
        );

        filteredSymptoms.forEach((symptom, index) => {
            const suggestionItem = document.createElement("div");
            suggestionItem.classList.add("suggestion-item");
            suggestionItem.textContent = symptom;
            suggestionItem.dataset.index = index;

            suggestionItem.addEventListener("click", function () {
                addSymptom(symptom);
            });

            suggestionsBox.appendChild(suggestionItem);
        });
    }

    // Add symptom to input box
    function addSymptom(symptom) {
        let currentInput = symptomInput.value;
        let symptomArray = currentInput.split(", ").map(s => s.trim());

        if (!symptomArray.includes(symptom)) {
            symptomArray.push(symptom);
            symptomInput.value = symptomArray.join(", ");
        }

        suggestionsBox.innerHTML = "";
    }

    // Debounce function to optimize performance
    function debounce(func, delay) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    }

    // Handle keyboard navigation
    function handleKeyDown(event) {
        const items = document.querySelectorAll(".suggestion-item");

        if (event.key === "ArrowDown") {
            selectedIndex = (selectedIndex + 1) % items.length;
            updateSelection(items);
        } else if (event.key === "ArrowUp") {
            selectedIndex = (selectedIndex - 1 + items.length) % items.length;
            updateSelection(items);
        } else if (event.key === "Enter" && selectedIndex !== -1) {
            event.preventDefault();
            if (filteredSymptoms[selectedIndex]) {
                addSymptom(filteredSymptoms[selectedIndex]);
            }
            selectedIndex = -1;
        }
    }

    // Highlight selected suggestion
    function updateSelection(items) {
        items.forEach((item, index) => {
            item.classList.toggle("selected", index === selectedIndex);
        });
    }

    // Event Listeners
    symptomInput.addEventListener("input", debounce(updateSuggestions, 300));
    symptomInput.addEventListener("keydown", handleKeyDown);

    document.addEventListener("click", function (event) {
        if (!symptomInput.contains(event.target) && !suggestionsBox.contains(event.target)) {
            suggestionsBox.innerHTML = "";
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const fadeInElements = document.querySelectorAll(".fade-in");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("show");
                }
            });
        },
        { threshold: 0.3 }
    );

    fadeInElements.forEach((el) => observer.observe(el));
});


