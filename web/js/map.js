window.onload = async () => {
  const stateNames = {
    "BAJA CALIFORNIA": "mx-bc",
    "BAJA CALIFORNIA SUR": "mx-bs",
    SONORA: "mx-so",
    COLIMA: "mx-cl",
    NAYARIT: "mx-na",
    CAMPECHE: "mx-cm",
    "QUINTANA ROO": "mx-qr",
    EDOMEX: "mx-mx",
    MORELIA: "mx-mo",
    CDMX: "mx-df",
    QUERETARO: "mx-qt",
    TABASCO: "mx-tb",
    CHIAPAS: "mx-cs",
    "NUEVO LEON": "mx-nl",
    SINALOA: "mx-si",
    CHIHUAHUA: "mx-ch",
    VERACRUZ: "mx-ve",
    ZACATECAS: "mx-za",
    AGUASCALIENTES: "mx-ag",
    JALISCO: "mx-ja",
    MICHOACAN: "mx-mi",
    OAXACA: "mx-oa",
    PUEBLA: "mx-pu",
    GUERRERO: "mx-gr",
    TLAXCALA: "mx-tl",
    TAMAULIPAS: "mx-tm",
    COAHUILA: "mx-co",
    YUCATAN: "mx-yu",
    DURANGO: "mx-dg",
    GUANAJUATO: "mx-gj",
    "SAN LUIS POTOSI": "mx-sl",
    HIDALGO: "mx-hg",
  };
  const codeToStateNames = Object.fromEntries(
    Object.entries(stateNames).map(([name, code]) => [code, name])
  );

  sancionometer_data = await fetch("/sancionometro.json")
    .then((response) => response.json())
    .then((data) => data);

  var data = Highcharts.geojson(Highcharts.maps["countries/mx/mx-all"]),
    separators = Highcharts.geojson(
      Highcharts.maps["countries/mx/mx-all"],
      "mapline"
    ),
    small = $("#container").width() < 400;

  var means = {};
  for (const element of sancionometer_data) {
    if (element.provenienteDe in means)
      means[element.provenienteDe].push(element);
    else means[element.provenienteDe] = [element];
  }
  var per_state_data = {};
  var per_state_mean = {};
  for (const key in stateNames) {
    if (Object.prototype.hasOwnProperty.call(stateNames, key)) {
      var mean_rating = 0;
      var list = means[key] ?? [];
      per_state_data[stateNames[key]] = [];
      list.forEach((element) => {
        var sumaTotal = element.sumaTotal;
        sumaTotal = sumaTotal / element.cantidadReportes;
        sumaTotal = sumaTotal + (element.cantidadReportes - 1) * 1.5;
        sumaTotal = Math.min(sumaTotal, 10);
        element.promedio = sumaTotal;
        mean_rating += sumaTotal;
        per_state_data[stateNames[key]].push(element);
      });
      var result = list.length == 0 ? 0 : mean_rating / list.length;
      per_state_mean[stateNames[key]] = result;
    }
  }
  $.each(data, function (i) {
    this.drilldown = this.properties["hc-key"];
    const mean_rating = per_state_mean[this.drilldown] ?? 0;
    this.value = parseFloat(mean_rating.toFixed(2));
  });

  Highcharts.mapChart("container", {
    chart: {
      backgroundColor: "gray",
      events: {
        drilldown: function (e) {
          if (!e.seriesOptions) {
            var chart = this;
            const mapKey = e.point.drilldown;
            const button = document.getElementById("showModal");
            const modalTitle = document.getElementById("exampleModalLabel");
            const modalBody = document.getElementById("modalBody");
            modalTitle.textContent = codeToStateNames[mapKey];
            string_builder =
              "<p style ='color:red'> busca cargo público nuevamente</p><br>";
            innner_data = per_state_data[mapKey];
            for (const element of per_state_data[mapKey]) {
              string_builder += `<p ${
                element.buscaCargo ? 'style = "color:red"' : ""
              }>Anónimo - ${element.promedio.toFixed(2)} - `;
              string_builder +=
                `${element.puesto?.[0][0] ?? element.actos?.[0][0]}` + "<br>";
              string_builder +=
                `${
                  element.sanciones?.[0][0] ?? element.resoluciones.join(" ,")
                }` + "<br><br></p>";
            }
            modalBody.innerHTML = string_builder;
            button.click();
          }
        },
      },
    },
    title: {
      text: "RiesgoCero",
      style: {
        color: "white",
      },
    },

    subtitle: {
      text: "Sancionómetro federal",
      floating: true,
      align: "center",
      y: 50,
      style: {
        color: "white",
        fontSize: "16px",
      },
    },

    legend: small
      ? {}
      : {
          layout: "horizontal",
          align: "center",
          horizontalAlign: "middle",
        },

    colorAxis: {
      min: 0,
      minColor: "#fffa9c",
      maxColor: "#ba0f0f",
    },

    mapNavigation: {
      enabled: true,
      buttonOptions: {
        verticalAlign: "bottom",
      },
    },

    plotOptions: {
      map: {
        states: {
          hover: {
            color: "#ffffff",
          },
        },
      },
    },

    series: [
      {
        data: data,
        name: "Sanción promedio",
        dataLabels: {
          enabled: true,
          format: "{point.properties.postal-code}",
        },
      },
      {
        type: "mapline",
        data: separators,
        color: "black",
        enableMouseTracking: false,
        animation: {
          duration: 500,
        },
      },
    ],

    drilldown: {
      activeDataLabelStyle: {
        color: "#FFFFFF",
        textDecoration: "none",
        textOutline: "1px #000000",
      },
      drillUpButton: {
        relativeTo: "spacingBox",
        position: {
          x: 0,
          y: 60,
        },
      },
    },
  });
};
