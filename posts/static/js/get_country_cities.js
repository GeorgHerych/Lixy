const countrySelect = document.getElementById('id_country');
const citySelect = document.getElementById('id_city');

function get_cities(countryId) {
    fetch(`/members/edit-profile/get-cities?country_id=${countryId}`)
        .then(response => response.json())
        .then(data => {
            const selectedCity = parseInt(citySelect.value);
            citySelect.innerHTML = '';

            const option = document.createElement('option');
            option.textContent = '---------';

            citySelect.appendChild(option);

            data.forEach(city => {
                const option = document.createElement('option');

                if (city.id === selectedCity) {
                    option.selected = true;
                }

                option.value = city.id;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        });
}

get_cities(countrySelect.value);

countrySelect.addEventListener('change', function () {
    const countryId = this.value;
    get_cities(countryId);
});