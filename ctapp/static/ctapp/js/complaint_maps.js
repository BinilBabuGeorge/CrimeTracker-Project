(function () {
  function toNumber(value) {
    if (value === null || value === undefined || value === "") {
      return null;
    }

    var parsed = parseFloat(value);
    return Number.isFinite(parsed) ? parsed : null;
  }

  function setCoordinateValue(input, value) {
    if (input) {
      input.value = value.toFixed(6);
    }
  }

  function updateCoordinateLabel(target, lat, lng) {
    if (!target) {
      return;
    }

    if (lat === null || lng === null) {
      target.textContent = "No location selected yet.";
      return;
    }

    target.textContent = "Selected coordinates: " + lat.toFixed(6) + ", " + lng.toFixed(6);
  }

  function initComplaintMap(element) {
    if (!window.L || !element) {
      return;
    }

    var mode = element.dataset.mode || "view";
    var latInput = element.dataset.latInput ? document.getElementById(element.dataset.latInput) : null;
    var lngInput = element.dataset.lngInput ? document.getElementById(element.dataset.lngInput) : null;
    var statusElement = element.dataset.statusId ? document.getElementById(element.dataset.statusId) : null;
    var defaultLat = toNumber(element.dataset.defaultLat);
    var defaultLng = toNumber(element.dataset.defaultLng);
    var initialLat = latInput ? toNumber(latInput.value) : toNumber(element.dataset.lat);
    var initialLng = lngInput ? toNumber(lngInput.value) : toNumber(element.dataset.lng);
    var hasInitialCoords = initialLat !== null && initialLng !== null;
    var startLat = hasInitialCoords ? initialLat : (defaultLat !== null ? defaultLat : 20.5937);
    var startLng = hasInitialCoords ? initialLng : (defaultLng !== null ? defaultLng : 78.9629);
    var startZoom = hasInitialCoords ? 15 : 5;
    var marker = null;

    var map = L.map(element).setView([startLat, startLng], startZoom);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
      maxZoom: 19,
    }).addTo(map);

    function bindMarkerDrag() {
      if (mode !== "picker" || !marker) {
        return;
      }

      marker.off("dragend");
      marker.on("dragend", function (event) {
        var position = event.target.getLatLng();
        setLocation(position.lat, position.lng, true, false);
      });
    }

    function setLocation(lat, lng, syncInputs, panMap) {
      if (marker) {
        marker.setLatLng([lat, lng]);
      } else {
        marker = L.marker([lat, lng], { draggable: mode === "picker" }).addTo(map);
        bindMarkerDrag();
      }

      if (syncInputs) {
        setCoordinateValue(latInput, lat);
        setCoordinateValue(lngInput, lng);
      }

      updateCoordinateLabel(statusElement, lat, lng);

      if (panMap) {
        map.setView([lat, lng], Math.max(map.getZoom(), 15));
      }
    }

    if (hasInitialCoords) {
      setLocation(initialLat, initialLng, false, false);
    } else {
      updateCoordinateLabel(statusElement, null, null);
    }

    if (mode === "picker") {
      map.on("click", function (event) {
        setLocation(event.latlng.lat, event.latlng.lng, true, false);
      });

      [latInput, lngInput].forEach(function (input) {
        if (!input) {
          return;
        }

        input.addEventListener("change", function () {
          var changedLat = latInput ? toNumber(latInput.value) : null;
          var changedLng = lngInput ? toNumber(lngInput.value) : null;

          if (changedLat !== null && changedLng !== null) {
            setLocation(changedLat, changedLng, false, true);
          }
        });
      });
    } else if (hasInitialCoords) {
      marker.bindPopup(element.dataset.popupText || "Complaint location").openPopup();
    }

    window.setTimeout(function () {
      map.invalidateSize();
    }, 150);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var maps = document.querySelectorAll(".leaflet-complaint-map");
    maps.forEach(initComplaintMap);
  });
})();
