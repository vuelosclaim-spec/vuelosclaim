(function () {
  "use strict";
  var cfg = window.CTT || {};
  var LANG = cfg.lang === "en" ? "en" : "es";
  var AIRLINES = cfg.airlines || [];
  var ALIAS_ES = {
    LHR: "Londres", LGW: "Londres", STN: "Londres", LTN: "Londres", LCY: "Londres", AMS: "Ámsterdam",
    BRU: "Bruselas", CRL: "Bruselas", CDG: "París", ORY: "París", BVA: "París", FCO: "Roma", CIA: "Roma",
    MXP: "Milán", BGY: "Milán", LIN: "Milán", MUC: "Múnich", BER: "Berlín", GVA: "Ginebra", ZRH: "Zúrich",
    LIS: "Lisboa", OPO: "Oporto", ATH: "Atenas", IST: "Estambul", SAW: "Estambul", JFK: "Nueva York",
    EWR: "Nueva York", CPH: "Copenhague", ARN: "Estocolmo", VIE: "Viena", WAW: "Varsovia", PRG: "Praga",
    DUB: "Dublín", EDI: "Edimburgo", MAN: "Mánchester", FRA: "Fráncfort", HAM: "Hamburgo", VCE: "Venecia",
    NAP: "Nápoles", FLR: "Florencia", RAK: "Marrakech", TFN: "Tenerife Norte", TFS: "Tenerife Sur",
    ACE: "Lanzarote", FUE: "Fuerteventura", LPA: "Gran Canaria", IBZ: "Ibiza", MAH: "Menorca",
    PMI: "Palma de Mallorca", SCQ: "Santiago de Compostela", BOG: "Bogotá", MEX: "Ciudad de México",
    EZE: "Buenos Aires", LIM: "Lima", MIA: "Miami", CUN: "Cancún", BCN: "Barcelona", MAD: "Madrid",
    VLC: "Valencia", AGP: "Málaga", ALC: "Alicante", SVQ: "Sevilla", BIO: "Bilbao", GRX: "Granada",
    XRY: "Jerez", VGO: "Vigo", OVD: "Asturias", SDR: "Santander", ZAZ: "Zaragoza", RMU: "Murcia",
    LEI: "Almería", REU: "Reus", GRO: "Girona", MLN: "Melilla", SPC: "La Palma", NCE: "Niza", MRS: "Marsella",
    LYS: "Lyon", TLS: "Toulouse", BOD: "Burdeos", NTE: "Nantes", GOT: "Gotemburgo", OSL: "Oslo",
    HEL: "Helsinki", BUD: "Budapest", OTP: "Bucarest", SOF: "Sofía", KRK: "Cracovia", DUS: "Düsseldorf",
    CGN: "Colonia", STR: "Stuttgart", BSL: "Basilea", MLA: "Malta", LCA: "Lárnaca", TLV: "Tel Aviv",
    CMN: "Casablanca", TNG: "Tánger", DXB: "Dubái", DOH: "Doha", GRU: "São Paulo", SCL: "Santiago de Chile",
    HAV: "La Habana", PUJ: "Punta Cana", SDQ: "Santo Domingo", CCS: "Caracas", UIO: "Quito", GYE: "Guayaquil"
  };
  var ALIAS_EN = {
    LHR: "London", LGW: "London", STN: "London", LTN: "London", LCY: "London", LPA: "Gran Canaria",
    TFS: "Tenerife South", TFN: "Tenerife North", PMI: "Palma de Mallorca", AGP: "Malaga", ALC: "Alicante",
    ACE: "Lanzarote", FUE: "Fuerteventura", IBZ: "Ibiza", MAH: "Menorca", SCQ: "Santiago de Compostela",
    OVD: "Asturias", SPC: "La Palma", MAD: "Madrid", BCN: "Barcelona", VLC: "Valencia", SVQ: "Seville",
    GRO: "Girona", REU: "Reus", RMU: "Murcia", LEI: "Almeria", XRY: "Jerez", GRX: "Granada",
    MAN: "Manchester", BHX: "Birmingham", BRS: "Bristol", EDI: "Edinburgh", GLA: "Glasgow", NCL: "Newcastle",
    LBA: "Leeds Bradford", EMA: "East Midlands", LPL: "Liverpool", BFS: "Belfast", DUB: "Dublin",
    JFK: "New York", EWR: "New York", BGY: "Milan", MXP: "Milan"
  };
  var T = {
    es: {
      regEU: "El vuelo sale de la UE, el EEE (Noruega, Islandia, Liechtenstein) o Suiza: se aplica el Reglamento (CE) 261/2004, sea cual sea la aerolínea.",
      reg3EU: "El vuelo llega a la UE desde fuera y lo operó una aerolínea europea: se aplica el Reglamento (CE) 261/2004.",
      reg3EUuk: "El vuelo llega a la UE desde fuera con una aerolínea británica: el reglamento europeo no lo cubre, pero sí la norma británica UK261 (en libras).",
      regUK: "El vuelo sale del Reino Unido: se aplica la norma británica UK261, en libras, sea cual sea la aerolínea.",
      regUKin: "El vuelo llega al Reino Unido desde fuera con una aerolínea británica o europea: se aplica UK261, en libras.",
      notIn: "El vuelo llega desde fuera de Europa con una aerolínea no europea ni británica: ni el reglamento europeo ni UK261 lo cubren.",
      not3: "El viaje ni sale ni llega a la UE, el EEE, Suiza o el Reino Unido: estas normas no lo cubren, aunque la aerolínea sea europea o haya una escala en Europa (TJUE, C-451/20).",
      carrierUnknown: "El vuelo llega desde fuera de Europa: solo está cubierto si lo operó una aerolínea europea (o británica, si llega al Reino Unido o a la UE con UK261).",
      mCarrier: "qué aerolínea operó el vuelo (aparece en la tarjeta de embarque; puede no ser la que te vendió el billete)",
      mixed: "Esta aerolínea tiene filiales europeas y británicas. Si el vuelo lo operó la británica, se aplica UK261 en libras en lugar del reglamento europeo.",
      operating: "Cuenta la aerolínea que operó el vuelo, no la que te vendió el billete.",
      alsoUK: "Al llegar al Reino Unido con una aerolínea británica o europea, también puede aplicarse UK261. Solo se cobra una vez.",
      alsoEU: "Al llegar a la UE con una aerolínea europea, también puede aplicarse el reglamento europeo (en euros). Solo se cobra una vez.",
      special: "Con estos datos no lo cubrirían ni el reglamento europeo ni UK261, pero no podemos descartarlo: depende de la licencia de la aerolínea que operó el vuelo y de normas locales que no hemos podido verificar.",
      mSpecial: "qué aerolínea operó el vuelo y quién le dio la licencia (la UE, el Reino Unido o una autoridad local); pregúntalo también a la autoridad de aviación local",
      crown: "Jersey, Guernsey, la isla de Man y Gibraltar no forman parte del Reino Unido ni de la UE: a efectos de ambas normas cuentan como origen o destino de fuera (art. 3).",
      gib: "Desde el 15-07-2026 se aplica el acuerdo UE–Reino Unido sobre Gibraltar. No hemos podido confirmar si cambia los derechos de los pasajeros en su aeropuerto.",
      lyr: "Svalbard queda fuera del Acuerdo sobre el Espacio Económico Europeo (Protocolo 40): cuenta como origen o destino de fuera del EEE.",
      ecn: "El derecho de la UE no se aplica en el norte de Chipre (Protocolo 10 del Acta de adhesión de 2003): el aeropuerto de Ercan cuenta como de fuera de la UE.",
      notUKcomm: "El vuelo llega al Reino Unido desde fuera con una aerolínea con licencia de Suiza, Noruega o Islandia: para UK261 no es aerolínea comunitaria ni británica, así que no lo cubre.",
      ukcommUnknown: "El vuelo llega al Reino Unido desde fuera: UK261 solo lo cubre si la aerolínea tiene licencia británica o de un país de la UE, y esta aerolínea tiene filiales con licencia de fuera de la UE.",
      mLicence: "qué filial de la aerolínea operó el vuelo y qué país le dio la licencia",
      viaMixed: "El viaje llega a Europa desde fuera con escalas en aerolíneas distintas: ningún tribunal ha aclarado qué aerolínea decide la cobertura en ese caso.",
      mViaMixed: "qué aerolínea operó cada tramo del viaje",
      viaSingle: "Con escalas en una sola reserva, el viaje cuenta entero: el retraso se mide al llegar al destino final y la distancia es la línea recta entre el origen y el destino final (TJUE, C-11/11, C-559/16 y C-451/20).",
      viaSeparate: "Con reservas separadas, cada vuelo se reclama por separado: pon el origen y el destino del vuelo que se retrasó o se canceló.",
      fareStaff: "Los billetes gratuitos o con una tarifa reducida que no está al alcance del público (por ejemplo, de empleado) quedan fuera del reglamento (art. 3.3). Los billetes de puntos o de paquete vacacional sí están cubiertos.",
      mStrikeSub: "quién contrató a la empresa en huelga y si la aerolínea pudo evitar el retraso (pídelo por escrito a la aerolínea)",
      exact3: "3 horas justas cuentan: el reglamento exige «tres horas o más», medidas al abrirse las puertas en el destino final (TJUE, C-402/07 y C-452/13). Con 2 h 59 min no hay compensación.",
      bands: ["hasta 1.500 km", "más de 1.500 km dentro de la UE", "entre 1.500 y 3.500 km", "más de 3.500 km"],
      dist: function (d, band, base) { return "Distancia: " + d + " km (" + band + ") → hasta " + base + " por pasajero."; },
      lt3: "Llegaste al destino final con menos de 3 horas de retraso: no hay compensación económica.",
      lt3note: "Aun así, según la distancia, a partir de 2, 3 o 4 horas de retraso en la salida la aerolínea te debe comida y bebida.",
      mDelay: "con cuánto retraso llegaste al destino final",
      full: "Llegaste al destino final con 3 horas o más de retraso: por regla general corresponde compensación (TJUE, Sturgeon, C-402/07).",
      half: function (m) { return "En vuelos de más de 3.500 km fuera de la UE con un retraso de 3 a 4 horas, la compensación se reduce a la mitad: " + m + " (art. 7.2)."; },
      arrival: "El retraso se mide en el destino final, cuando se abren las puertas del avión (TJUE, C-452/13).",
      gt14: "Te avisaron de la cancelación con 14 días o más de antelación: no hay compensación (art. 5.1.c.i).",
      gt14note: "Sí tienes derecho a elegir entre el reembolso del billete o un vuelo alternativo.",
      mNotice: "con cuántos días de antelación te avisaron de la cancelación",
      n7to14: "Aviso de entre 7 y 13 días: la aerolínea solo se libra si te ofreció un vuelo alternativo que saliera como mucho 2 horas antes y llegara menos de 4 horas después que el original (art. 5.1.c.ii).",
      nlt7: "Aviso de menos de 7 días: la aerolínea solo se libra si te ofreció un vuelo alternativo que saliera como mucho 1 hora antes y llegara menos de 2 horas después que el original (art. 5.1.c.iii).",
      rerouteNo: "No te ofrecieron un vuelo alternativo: esa excepción no se aplica.",
      mReroute: "si te ofrecieron un vuelo alternativo",
      mRerouteTimes: "a qué hora salía y llegaba el vuelo alternativo comparado con el original",
      exempt: "El vuelo alternativo que te ofrecieron cumple esos márgenes: no hay compensación.",
      exemptNote: "Mantienes el derecho al reembolso o al vuelo alternativo, y a la asistencia mientras esperas.",
      notExempt: "El vuelo alternativo que te ofrecieron no cumple esos márgenes: la excepción no se aplica.",
      accepted: "Aceptaste el vuelo alternativo: eso no te quita la compensación.",
      rejected: "Rechazaste el vuelo alternativo: puedes pedir el reembolso del billete además de la compensación.",
      reduced: function (m) { return "Como el vuelo alternativo llegó con poco retraso, la aerolínea puede reducir la compensación a la mitad: " + m + " (art. 7.2)."; },
      reduceMaybe: function (m) { return "Si el vuelo alternativo llegó como mucho 3 horas después del original, la aerolínea puede reducirla a la mitad: " + m + " (art. 7.2)."; },
      vol: "Cediste tu plaza voluntariamente: no hay compensación fija. Te corresponde lo que pactaste con la aerolínea, más el reembolso o un vuelo alternativo (art. 4.1).",
      mVol: "si cediste la plaza voluntariamente o te la negaron contra tu voluntad",
      checkinNo: "Para tener derecho hay que presentarse a facturación y embarque a tiempo (art. 3.2). Si llegaste tarde, no hay compensación.",
      mCheckin: "si te presentaste a tiempo a facturación y embarque, con la documentación en regla",
      reasonable: "Si te negaron el embarque por motivos razonables (salud, seguridad o documentación de viaje incorrecta), no hay compensación (art. 2.j).",
      overbook: "Te negaron el embarque contra tu voluntad por overbooking u otro motivo operativo: corresponde compensación (art. 4.3).",
      reasonUnknown: "No te explicaron el motivo: la denegación da derecho a compensación salvo motivos razonables de salud, seguridad o documentación (TJUE, C-321/11).",
      deniedNoExtra: "En la denegación de embarque la aerolínea no puede alegar circunstancias extraordinarias (TJUE, C-22/11).",
      c: {
        unknown: "No te dieron un motivo. La aerolínea solo se libra si demuestra una circunstancia extraordinaria que no pudo evitar con medidas razonables (art. 5.3).",
        tech: "Las averías del avión detectadas en el mantenimiento o en la operación normal no eximen de pagar (TJUE, C-549/07). Solo un defecto oculto de fabricación reconocido por el fabricante o las autoridades podría hacerlo (C-257/14).",
        crew: "La falta de tripulación o la enfermedad repentina de un tripulante no es una circunstancia extraordinaria (TJUE, C-156/22 a C-158/22).",
        strike_own: "La huelga del personal de la propia aerolínea no la exime de pagar (TJUE, C-28/20).",
        strike_ext: "Una huelga de controladores aéreos o del personal del aeropuerto puede ser circunstancia extraordinaria (Directrices de la Comisión de 2024, punto 5.2.3).",
        strike_sub: "No está resuelto si la huelga de una empresa que trabaja para la aerolínea (asistencia en tierra, catering, limpieza) es circunstancia extraordinaria: ni el TJUE ni las directrices de la Comisión lo aclaran.",
        weather: "Una meteorología incompatible con la seguridad del vuelo puede ser circunstancia extraordinaria.",
        atc: "Una restricción del control del tráfico aéreo no exime por sí sola: la aerolínea debe identificar la causa de fondo y demostrar que era extraordinaria, y solo descuenta el retraso que se deba a ella (TJUE, C-108/26, 2026).",
        security: "Los riesgos para la seguridad (amenazas, cierre del espacio aéreo, inestabilidad política) son circunstancias extraordinarias.",
        bird: "El choque con un ave o un objeto en la pista se considera circunstancia extraordinaria (TJUE, C-315/15 y C-501/17).",
        knock: "Si el retraso viene de un vuelo anterior del mismo avión, solo exime si en ese vuelo hubo una circunstancia extraordinaria y fue la causa directa de tu retraso, no una decisión propia de la aerolínea, como esperar a pasajeros de otro vuelo (TJUE, C-74/19; Tribunal General, T-656/24, 2026).",
        extra: "La aerolínea alega una circunstancia extraordinaria. Si la demuestra, no tiene que pagar."
      },
      strikeOwnNote: "Excepción: que las reivindicaciones de la huelga solo pudieran atenderlas las autoridades públicas.",
      mAtc: "qué provocó la restricción de control aéreo (pídeselo por escrito a la aerolínea)",
      mKnock: "qué causó el retraso del vuelo anterior (pídeselo por escrito a la aerolínea)",
      extraNote: function (m) { return "La aerolínea tiene que demostrarlo y probar que tomó todas las medidas razonables. Si no lo consigue (por ejemplo, otros vuelos salieron con normalidad), podrían corresponderte " + m + " por pasajero."; },
      hPos: function (m) { return "Posible derecho a compensación: hasta " + m + " por pasajero"; },
      hNo: "No parece corresponder compensación",
      hIns: "Información insuficiente para determinarlo",
      insAmt: function (m) { return "Si los datos que faltan te son favorables, podrían corresponderte hasta " + m + " por pasajero."; },
      missing: "Falta saber: ",
      letterLater: "Cuando completes los datos que faltan podrás generar una carta de reclamación.",
      loading: "Cargando la lista de aeropuertos…",
      acLoading: "Cargando aeropuertos… un momento.",
      acError: "No se ha podido cargar la lista de aeropuertos. Pulsa «Reintentar» más abajo.",
      acNone: "No encontramos ese aeropuerto. Prueba con la ciudad, el nombre o el código de 3 letras (MAD, BCN…).",
      pick: "Elige el aeropuerto en la lista que aparece al escribir.",
      acCount: function (n) { return (n === 1 ? "1 aeropuerto encontrado" : n + " aeropuertos encontrados") + ". Usa las flechas arriba y abajo para elegir y pulsa Intro."; },
      tableScroll: "tabla desplazable",
      same: "El origen y el destino son el mismo aeropuerto.",
      loadError: "No se ha podido cargar la lista de aeropuertos. Comprueba tu conexión y vuelve a intentarlo.",
      offline: "Parece que no tienes conexión. Cuando vuelva, la lista de aeropuertos se cargará sola.",
      copied: "Carta copiada. Pégala en el formulario o el correo de la aerolínea.",
      selected: "Texto seleccionado: cópialo con Ctrl+C o mantén pulsado.",
      downloaded: "Carta descargada.", dlFail: "No se ha podido descargar. Usa el botón de copiar.",
      file: "reclamacion-vuelo.txt"
    },
    en: {
      regEU: "The flight departs from the EU, the EEA (Norway, Iceland, Liechtenstein) or Switzerland, so Regulation (EC) 261/2004 applies whatever the airline.",
      reg3EU: "The flight arrives in the EU from outside and was operated by a European airline, so Regulation (EC) 261/2004 applies.",
      reg3EUuk: "The flight arrives in the EU from outside with a UK airline: EU261 does not cover it, but the UK rules (UK261, in pounds) do.",
      regUK: "The flight departs from the UK, so the UK rules (UK261) apply, in pounds, whatever the airline.",
      regUKin: "The flight arrives in the UK from outside with a UK or European airline, so UK261 applies, in pounds.",
      notIn: "The flight arrives from outside Europe with a non-European, non-UK airline, so neither EU261 nor UK261 covers it.",
      not3: "The journey neither departs from nor arrives in the EU, EEA, Switzerland or the UK, so these rules do not cover it, even with a European airline or a stopover in Europe (CJEU, C-451/20).",
      carrierUnknown: "The flight arrives from outside Europe, so it is only covered if a European airline operated it (or a UK airline, under UK261).",
      mCarrier: "which airline operated the flight (it's on the boarding pass; it may not be the one that sold you the ticket)",
      mixed: "This airline has both European and UK companies. If the UK company operated the flight, UK261 applies in pounds instead of EU261.",
      operating: "What counts is the airline that operated the flight, not the one that sold the ticket.",
      alsoUK: "Arriving in the UK with a UK or European airline, UK261 may also apply. You can only be paid once.",
      alsoEU: "Arriving in the EU with a European airline, EU261 (in euros) may also apply. You can only be paid once.",
      special: "On these details neither EU261 nor UK261 would cover it, but we can't rule it out: it depends on the licence of the airline that operated the flight and on local rules we have not been able to verify.",
      mSpecial: "which airline operated the flight and who licensed it (the EU, the UK or a local authority); also ask the local aviation authority",
      crown: "Jersey, Guernsey, the Isle of Man and Gibraltar are part of neither the UK nor the EU, so both sets of rules treat them as places outside (Art. 3).",
      gib: "The EU–UK agreement on Gibraltar has applied since 15 July 2026. We have not been able to confirm whether it changes passenger rights at its airport.",
      lyr: "Svalbard is outside the European Economic Area Agreement (Protocol 40), so it counts as outside the EEA.",
      ecn: "EU law does not apply in northern Cyprus (Protocol 10 to the 2003 Act of Accession), so Ercan airport counts as outside the EU.",
      notUKcomm: "The flight arrives in the UK from outside with an airline licensed in Switzerland, Norway or Iceland. For UK261 that is neither an EU nor a UK carrier, so UK261 does not cover it.",
      ukcommUnknown: "The flight arrives in the UK from outside. UK261 only covers it if the airline holds a UK or EU licence, and this airline has companies licensed outside the EU.",
      mLicence: "which company of the airline group operated the flight and which country licensed it",
      viaMixed: "The journey arrives in Europe from outside with connections on different airlines. No court has settled which airline decides coverage in that case.",
      mViaMixed: "which airline operated each leg of the journey",
      viaSingle: "Connections on a single booking count as one journey: the delay is measured at your final destination and the distance is the straight line from origin to final destination (CJEU, C-11/11, C-559/16 and C-451/20).",
      viaSeparate: "With separate bookings, each flight is claimed separately: enter the origin and destination of the flight that was delayed or cancelled.",
      fareStaff: "Free tickets, or reduced fares not available to the public (staff tickets, for example), are outside the rules (Art. 3(3)). Frequent-flyer and package holiday tickets are covered.",
      mStrikeSub: "who hired the company on strike and whether the airline could have avoided the delay (ask the airline in writing)",
      exact3: "Exactly 3 hours counts: the rules require 'three hours or more', measured when the doors open at your final destination (CJEU, C-402/07 and C-452/13). At 2 h 59 min there is no compensation.",
      bands: ["up to 1,500 km", "over 1,500 km within the EU", "1,500 to 3,500 km", "over 3,500 km"],
      dist: function (d, band, base) { return "Distance: " + d + " km (" + band + ") → up to " + base + " per passenger."; },
      lt3: "You reached your final destination less than 3 hours late, so there is no cash compensation.",
      lt3note: "Even so, depending on the distance, from 2, 3 or 4 hours' departure delay the airline owes you food and drinks.",
      mDelay: "how late you arrived at your final destination",
      full: "You reached your final destination 3 or more hours late, so compensation is generally due (CJEU, Sturgeon, C-402/07).",
      half: function (m) { return "On flights over 3,500 km outside the EU with a 3 to 4 hour delay, compensation is halved: " + m + " (Art. 7(2))."; },
      arrival: "The delay is measured at your final destination, when the aircraft doors open (CJEU, C-452/13).",
      gt14: "You were told about the cancellation 14 or more days in advance, so there is no compensation (Art. 5(1)(c)(i)).",
      gt14note: "You can still choose between a refund or an alternative flight.",
      mNotice: "how many days before departure you were told about the cancellation",
      n7to14: "Notice of 7 to 13 days: the airline is only exempt if it offered you an alternative flight leaving no more than 2 hours earlier and arriving less than 4 hours later than the original (Art. 5(1)(c)(ii)).",
      nlt7: "Notice of less than 7 days: the airline is only exempt if it offered you an alternative flight leaving no more than 1 hour earlier and arriving less than 2 hours later than the original (Art. 5(1)(c)(iii)).",
      rerouteNo: "You were not offered an alternative flight, so that exemption does not apply.",
      mReroute: "whether you were offered an alternative flight",
      mRerouteTimes: "when the alternative flight left and arrived compared with the original",
      exempt: "The alternative flight you were offered is within those limits, so there is no compensation.",
      exemptNote: "You keep the right to a refund or the alternative flight, and to care while you wait.",
      notExempt: "The alternative flight you were offered is outside those limits, so the exemption does not apply.",
      accepted: "You accepted the alternative flight: that does not cancel your compensation.",
      rejected: "You turned down the alternative flight: you can claim a refund of the ticket as well as compensation.",
      reduced: function (m) { return "Because the alternative flight arrived only a little late, the airline may halve the compensation: " + m + " (Art. 7(2))."; },
      reduceMaybe: function (m) { return "If the alternative flight arrived no more than 3 hours after the original, the airline may halve it: " + m + " (Art. 7(2))."; },
      vol: "You gave up your seat voluntarily, so there is no fixed compensation. You are owed what you agreed with the airline, plus a refund or an alternative flight (Art. 4(1)).",
      mVol: "whether you gave up your seat voluntarily or were denied boarding against your will",
      checkinNo: "To qualify you must have checked in and turned up for boarding on time (Art. 3(2)). If you were late, there is no compensation.",
      mCheckin: "whether you checked in and turned up for boarding on time, with valid travel documents",
      reasonable: "If you were denied boarding for reasonable grounds (health, safety, security or invalid travel documents), there is no compensation (Art. 2(j)).",
      overbook: "You were denied boarding against your will because of overbooking or another operational reason, so compensation applies (Art. 4(3)).",
      reasonUnknown: "No reason was given: denied boarding gives a right to compensation unless there were reasonable grounds of health, safety, security or documents (CJEU, C-321/11).",
      deniedNoExtra: "For denied boarding the airline cannot rely on extraordinary circumstances (CJEU, C-22/11).",
      c: {
        unknown: "No reason was given. The airline is only exempt if it proves extraordinary circumstances it could not have avoided with reasonable measures (Art. 5(3)).",
        tech: "Technical faults found during maintenance or normal operation do not exempt the airline (CJEU, C-549/07). Only a hidden manufacturing defect confirmed by the manufacturer or the authorities might (C-257/14).",
        crew: "Crew shortages or a crew member's sudden illness are not extraordinary circumstances (CJEU, C-156/22 to C-158/22).",
        strike_own: "A strike by the airline's own staff does not exempt it from paying (CJEU, C-28/20).",
        strike_ext: "A strike by air traffic controllers or airport staff may be an extraordinary circumstance (Commission guidelines of 2024, point 5.2.3).",
        strike_sub: "It is not settled whether a strike at a company working for the airline (ground handling, catering, cleaning) is an extraordinary circumstance: neither the CJEU nor the Commission guidelines say.",
        weather: "Weather that makes flying unsafe can be an extraordinary circumstance.",
        atc: "An air traffic control restriction is not an exemption in itself: the airline must identify the underlying cause and prove it was extraordinary, and can only discount the delay it caused (CJEU, C-108/26, 2026).",
        security: "Security risks (threats, airspace closures, political instability) are extraordinary circumstances.",
        bird: "A bird strike or an object on the runway is an extraordinary circumstance (CJEU, C-315/15 and C-501/17).",
        knock: "If the delay came from an earlier flight by the same aircraft, it only exempts the airline if that flight was hit by an extraordinary circumstance that directly caused your delay, not by the airline's own choice, such as waiting for passengers from another flight (CJEU, C-74/19; General Court, T-656/24, 2026).",
        extra: "The airline claims extraordinary circumstances. If it proves them, it does not have to pay."
      },
      strikeOwnNote: "Exception: if the strikers' demands could only be met by the public authorities.",
      mAtc: "what caused the air traffic control restriction (ask the airline in writing)",
      mKnock: "what caused the earlier flight's delay (ask the airline in writing)",
      extraNote: function (m) { return "The airline has to prove it and show it took all reasonable measures. If it can't (for example, other flights left normally), you could be owed " + m + " per passenger."; },
      hPos: function (m) { return "Possible right to compensation: up to " + m + " per passenger"; },
      hNo: "Compensation does not appear to be due",
      hIns: "Not enough information to decide",
      insAmt: function (m) { return "If the missing details go your way, you could be owed up to " + m + " per passenger."; },
      missing: "Still needed: ",
      letterLater: "Once you fill in the missing details you'll be able to generate a claim letter.",
      loading: "Loading the airport list…",
      acLoading: "Loading airports… one moment.",
      acError: "The airport list could not load. Press “Try again” below.",
      acNone: "We can't find that airport. Try the city, the airport name or its 3-letter code (LHR, MAN…).",
      pick: "Choose the airport from the list that appears as you type.",
      acCount: function (n) { return (n === 1 ? "1 airport found" : n + " airports found") + ". Use the up and down arrows to choose and press Enter."; },
      tableScroll: "scrollable table",
      same: "Departure and destination are the same airport.",
      loadError: "The airport list could not load. Check your connection and try again.",
      offline: "You seem to be offline. The airport list will load by itself when you reconnect.",
      copied: "Letter copied. Paste it into the airline's claim form or email.",
      selected: "Text selected: copy it with Ctrl+C or a long press.",
      downloaded: "Letter downloaded.", dlFail: "Download failed. Use the copy button instead.",
      file: "flight-claim.txt"
    }
  };
  var TT = T; // both languages, for tests
  T = T[LANG];
  var airports = [], byCode = {};

  // ---------- Measurement: GA4 events, only after consent and never with personal data ----------
  // Only these parameters, with values from fixed lists (incident type, result, amount band...), ever leave the page.
  var TRACK_KEYS = { incident_type: 1, result: 1, compensation_category: 1, affiliate_id: 1, placement: 1, regime: 1 };
  function track(name, params) {
    try {
      if (!window.vcAnalytics || typeof window.gtag !== "function") return false;
      // site_language/source_page: "language" and "page_path" are reserved by GA4 and would overwrite the browser language and page path
      var q = { site_language: LANG, source_page: location.pathname };
      for (var k in params) if (TRACK_KEYS[k] && params[k] != null && params[k] !== "") q[k] = String(params[k]).replace(/[^\w.-]/g, "_").slice(0, 40);
      window.gtag("event", name, q);
      return true;
    } catch (e) { return false; /* measurement must never break the page */ }
  }
  function affId(href) {
    try {
      var h = new URL(href).hostname.replace(/^www\./, "");
      return { "airhelp.tpx.gr": "airhelp_tp", "compensair.tpx.gr": "compensair_tp" }[h] || h;
    } catch (e) { return "unknown"; }
  }

  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function cityOf(a) { return (LANG === "en" ? ALIAS_EN[a[0]] : ALIAS_ES[a[0]]) || a[2] || a[1]; }
  function label(a) { return cityOf(a) + " (" + a[0] + ")"; }
  function km(a, b) {
    var R = 6371, r = Math.PI / 180;
    var dLat = (b[4] - a[4]) * r, dLon = (b[5] - a[5]) * r;
    var h = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a[4] * r) * Math.cos(b[4] * r) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return Math.round(2 * R * Math.asin(Math.sqrt(h)));
  }
  function fmt(n) { return n.toLocaleString(LANG === "en" ? "en-GB" : "es-ES"); }
  function money(n, cur) {
    if (LANG === "en") return (cur === "GBP" ? "£" : "€") + fmt(n);
    return fmt(n) + (cur === "GBP" ? " £" : " €");
  }
  var UK = { GB: 1, GG: 1, JE: 1, IM: 1 };           // used by the airport search (home results)
  // Territories with a verified special status (see fuente/PRECISION_JURIDICA.md):
  // Jersey, Guernsey, Isle of Man and Gibraltar are neither the UK nor the EU, so both regimes treat them as "third countries".
  var CROWN = { GG: 1, JE: 1, IM: 1, GI: 1 };
  // Airports in EU/EEA states where the treaties do not apply: Svalbard (EEA Agreement, Protocol 40) and Ercan
  // (northern Cyprus, acquis suspended by Protocol 10 to the 2003 Act of Accession).
  var OUTSIDE = { LYR: 1, ECN: 1 };
  function inEU(a) { return a[6] === 1 && !OUTSIDE[a[0]]; }
  // Where a "not covered" result may hide local rules or carriers we cannot verify, we answer "insufficient", never "no".
  function unsure(a) { return !!(CROWN[a[3]] || a[0] === "LYR"); }

  // ---------- Rule engine: EU261 (Regulation (EC) 261/2004) and UK261 ----------
  // Three results: "posible" (possible right to compensation), "no" (does not appear to be due),
  // "insuficiente" (not enough information). `amount` is the potential amount, never a promise.
  // Inputs: dep, arr (airport tuples), airline {eu: yes|no|mixed|unknown, uk: bool}, what: delay|cancel|denied,
  // delay: lt3|3to4|gt4|unknown or delayMin (minutes late at final destination),
  // notice: gt14|7to14|lt7|unknown or noticeDays, reroute: yes|no|unknown, rdep: le1|1to2|gt2|unknown or
  // rerouteDepEarlyMin (minutes the alternative left before the original; 0 or less = same time or later),
  // rarr: lt2|2to4|ge4|unknown or rerouteArrLateMin, accepted: yes|no|unknown,
  // denied: invol|vol|unknown, checkin: yes|no|unknown, dreason: overbooking|reasonable|unknown,
  // cause: unknown|tech|crew|strike_own|strike_ext|weather|atc|security|bird|knock, distKm (optional override).
  var RANK = { posible: 0, insuficiente: 1, no: 2 };
  function compute(o, lang) {
    var t = lang ? TT[lang] : T;
    var r = { verdict: "posible", amount: 0, potential: 0, cur: "EUR", regime: null, covered: false, intra: false,
      lines: [], notes: [], missing: [], dist: 0, full: 0 };
    var st = "posible";
    function worse(s) { if (RANK[s] > RANK[st]) st = s; }
    function miss(m) { if (r.missing.indexOf(m) < 0) r.missing.push(m); }
    var dep = o.dep, arr = o.arr;
    r.dist = typeof o.distKm === "number" ? o.distKm : km(dep, arr);

    // 1. Territorial scope (the operating carrier, not the airline's nationality, decides inbound flights only)
    var al = o.airline || {}, eu = al.eu || "unknown", ukc = !!al.uk;
    var dEU = inEU(dep), aEU = inEU(arr);
    var dUK = dep[3] === "GB", aUK = arr[3] === "GB";
    // UK261 "Community carrier" = licence from an EU Member State (not Switzerland, Norway or Iceland).
    var euUK = (eu === "yes" || eu === "mixed") ? (al.ukcomm === false ? false : al.ukcomm === "unknown" ? null : true)
      : eu === "unknown" ? null : false;
    var euOrUk = ukc ? true : euUK;
    var out = false; // not covered by either regime
    if (dEU) {
      r.regime = "EU"; r.covered = true; r.intra = aEU; r.lines.push(t.regEU);
      if (aUK && euOrUk === true) r.notes.push(t.alsoUK);
    } else if (dUK) {
      r.regime = "UK"; r.covered = true; r.intra = aUK; r.lines.push(t.regUK);
      if (aEU && (eu === "yes" || eu === "mixed")) r.notes.push(t.alsoEU);
    } else if (aEU) {
      if (eu === "yes" || eu === "mixed") { r.regime = "EU"; r.covered = true; r.lines.push(t.reg3EU); if (eu === "mixed") r.notes.push(t.mixed); }
      else if (ukc) { r.regime = "UK"; r.covered = true; r.lines.push(t.reg3EUuk); }
      else if (eu === "no") { r.lines.push(t.notIn); out = true; }
      else { r.regime = "EU"; r.covered = null; r.lines.push(t.carrierUnknown); miss(t.mCarrier); worse("insuficiente"); }
      r.notes.push(t.operating);
    } else if (aUK) {
      if (euOrUk === true) { r.regime = "UK"; r.covered = true; r.lines.push(t.regUKin); }
      else if (euOrUk === false) { r.lines.push(al.ukcomm === false && eu !== "no" ? t.notUKcomm : t.notIn); out = true; }
      else if (eu === "yes" || eu === "mixed") { r.regime = "UK"; r.covered = null; r.lines.push(t.ukcommUnknown); miss(t.mLicence); worse("insuficiente"); }
      else { r.regime = "UK"; r.covered = null; r.lines.push(t.carrierUnknown); miss(t.mCarrier); worse("insuficiente"); }
      r.notes.push(t.operating);
    } else { r.lines.push(t.not3); out = true; }
    var uns = unsure(dep) || unsure(arr);
    var via = o.via || "direct";
    // Inbound journey with connections on different airlines: no case law says which leg's carrier decides (art. 3(1)(b))
    var mixedIn = via === "mixed" && !dEU && !dUK && (aEU || aUK);
    if (out && !uns && !mixedIn) { r.verdict = "no"; return r; }
    if (out) { r.regime = (CROWN[dep[3]] || CROWN[arr[3]] || dUK || aUK) ? "UK" : "EU"; r.covered = null; }
    if (out && uns) { r.lines.push(t.special); miss(t.mSpecial); worse("insuficiente"); }
    if (mixedIn) { r.lines.push(t.viaMixed); miss(t.mViaMixed); worse("insuficiente"); }
    if (CROWN[dep[3]] || CROWN[arr[3]]) r.notes.push(t.crown);
    if (dep[3] === "GI" || arr[3] === "GI") r.notes.push(t.gib);
    if (dep[0] === "LYR" || arr[0] === "LYR") r.notes.push(t.lyr);
    if (dep[0] === "ECN" || arr[0] === "ECN") r.notes.push(t.ecn);
    // Connections on a single booking count as one journey (CJEU C-451/20; UK261 art. 3(1A))
    if (via === "separate") r.notes.push(t.viaSeparate);
    else if (via !== "direct") r.notes.push(t.viaSingle);
    // Art. 3(3): free or non-public reduced fares are excluded; frequent-flyer and package tickets are covered
    if (o.fare === "staff") { r.lines.push(t.fareStaff); r.verdict = "no"; return r; }
    if (r.regime === "UK") r.cur = "GBP";

    // 2. Amount by great-circle distance to the final destination (Art. 7(1))
    var tiers = r.regime === "UK" ? [220, 350, 520] : [250, 400, 600];
    var d = r.dist, tier = d <= 1500 ? 0 : (r.intra || d <= 3500) ? 1 : 2;
    var base = tiers[tier], amount = base;
    var band = tier === 0 ? t.bands[0] : r.intra && d > 3500 ? t.bands[1] : tier === 1 ? t.bands[2] : t.bands[3];
    r.lines.push(t.dist(fmt(d), band, money(base, r.cur)));

    // 3. What happened
    var useCause = true;
    if (o.what === "delay") {
      var dl = typeof o.delayMin === "number" ? (o.delayMin < 180 ? "lt3" : o.delayMin <= 240 ? "3to4" : "gt4") : (o.delay || "unknown");
      if (dl === "lt3") { r.lines.push(t.lt3); r.notes.push(t.exact3); r.notes.push(t.lt3note); r.verdict = "no"; return r; }
      if (dl === "unknown") { miss(t.mDelay); worse("insuficiente"); }
      else if (dl === "3to4" && tier === 2) { amount = base / 2; r.lines.push(t.half(money(amount, r.cur))); }
      else r.lines.push(t.full);
      if (dl === "3to4") r.notes.push(t.exact3);
      r.notes.push(t.arrival);
    } else if (o.what === "cancel") {
      var nd = typeof o.noticeDays === "number" ? (o.noticeDays >= 14 ? "gt14" : o.noticeDays >= 7 ? "7to14" : "lt7") : (o.notice || "unknown");
      if (nd === "gt14") { r.lines.push(t.gt14); r.notes.push(t.gt14note); r.verdict = "no"; return r; }
      if (nd === "unknown") { miss(t.mNotice); worse("insuficiente"); }
      else {
        r.lines.push(nd === "7to14" ? t.n7to14 : t.nlt7);
        var rr = o.reroute || "unknown";
        if (rr === "no") r.lines.push(t.rerouteNo);
        else if (rr === "unknown") { miss(t.mReroute); worse("insuficiente"); }
        else {
          var early = typeof o.rerouteDepEarlyMin === "number" ? o.rerouteDepEarlyMin
            : { le1: 60, "1to2": 120, gt2: 121 }[o.rdep];
          var late = typeof o.rerouteArrLateMin === "number" ? o.rerouteArrLateMin
            : { lt2: 119, "2to4": 239, ge4: 240 }[o.rarr];
          var lim = nd === "7to14" ? [120, 240] : [60, 120];
          // With chips, "2to4" is 120–239 min: below 240 (exempt for 7–13 days), at least 120 (not exempt for <7 days).
          if (typeof o.rerouteArrLateMin !== "number" && o.rarr === "2to4") late = nd === "7to14" ? 239 : 120;
          if (typeof o.rerouteDepEarlyMin !== "number" && o.rdep === "1to2") early = nd === "7to14" ? 120 : 61;
          var depOk = early === undefined ? null : early <= lim[0];
          var arrOk = late === undefined ? null : late < lim[1];
          if (depOk === false || arrOk === false) r.lines.push(t.notExempt);
          else if (depOk && arrOk) { r.lines.push(t.exempt); r.notes.push(t.exemptNote); r.verdict = "no"; return r; }
          else { miss(t.mRerouteTimes); worse("insuficiente"); }
          if (o.accepted === "yes") r.notes.push(t.accepted);
          else if (o.accepted === "no") r.notes.push(t.rejected);
          // Art. 7(2): halved if the re-routed arrival is within 2 / 3 / 4 h depending on the distance band
          var cap = [120, 180, 240][tier];
          if (typeof o.rerouteArrLateMin === "number") {
            if (o.rerouteArrLateMin <= cap) { amount = base / 2; r.lines.push(t.reduced(money(amount, r.cur))); }
          } else if (o.rarr === "lt2" || (o.rarr === "2to4" && tier === 2)) { amount = base / 2; r.lines.push(t.reduced(money(amount, r.cur))); }
          else if (o.rarr === "2to4" && tier === 1) r.notes.push(t.reduceMaybe(money(base / 2, r.cur)));
        }
      }
    } else if (o.what === "denied") {
      useCause = false;
      var dv = o.denied || "unknown";
      if (dv === "vol") { r.lines.push(t.vol); r.verdict = "no"; return r; }
      if (dv === "unknown") { miss(t.mVol); worse("insuficiente"); }
      if (o.dreason === "reasonable") { r.lines.push(t.reasonable); r.verdict = "no"; return r; }
      if (o.checkin === "no") { r.lines.push(t.checkinNo); r.verdict = "no"; return r; }
      if (o.checkin !== "yes") { miss(t.mCheckin); worse("insuficiente"); }
      r.lines.push(o.dreason === "overbooking" ? t.overbook : t.reasonUnknown);
      r.notes.push(t.deniedNoExtra);
    }

    // 4. Cause (Art. 5(3) and case law); does not apply to denied boarding
    if (useCause) {
      var c = { strike: "strike_own", extra: "extra" }[o.cause] || o.cause || "unknown";
      if (!t.c[c]) c = "unknown";
      r.lines.push(t.c[c]);
      if (c === "strike_own") r.notes.push(t.strikeOwnNote);
      if (c === "atc") { miss(t.mAtc); worse("insuficiente"); }
      if (c === "strike_sub") { miss(t.mStrikeSub); worse("insuficiente"); }
      if (c === "knock") { miss(t.mKnock); worse("insuficiente"); }
      if (c === "strike_ext" || c === "weather" || c === "security" || c === "bird" || c === "extra") {
        r.potential = amount; r.notes.push(t.extraNote(money(amount, r.cur)));
        r.verdict = "no"; return r;
      }
    }
    r.verdict = st;
    r.amount = amount; r.potential = amount; r.full = base;
    if (st === "insuficiente") r.notes.unshift(t.insAmt(money(amount, r.cur)));
    return r;
  }
  window.CTT_compute = compute; // exposed for tests
  window.CTT_strings = TT;

  // ---------- Autocomplete ----------
  // Accepts IATA codes, city names (also Spanish/English aliases) and airport names, accents and case ignored.
  // Every airport is scored before sorting, so an exact code is never lost among many partial matches.
  var loadState = "loading"; // loading | ready | error
  function haystack(a) { return a._h || (a._h = norm([a[0], a[1], a[2], ALIAS_ES[a[0]] || "", ALIAS_EN[a[0]] || ""].join(" "))); }
  function search(q) {
    q = norm(q.trim()).replace(/[()]/g, " ").replace(/\s+/g, " ").trim();
    if (!q) return [];
    var words = q.split(" "), out = [];
    for (var i = 0; i < airports.length; i++) {
      var a = airports[i], code = a[0].toLowerCase();
      var es = norm(ALIAS_ES[a[0]] || ""), en = norm(ALIAS_EN[a[0]] || ""), city = norm(a[2]), name = norm(a[1]);
      var score = -1;
      if (code === q) score = 100;
      else if (norm(cityOf(a)) === q || es === q || en === q || city === q) score = 85;
      else if (norm(cityOf(a)).indexOf(q) === 0) score = 80;
      else if (es.indexOf(q) === 0 || en.indexOf(q) === 0 || city.indexOf(q) === 0) score = 70;
      else if (name.indexOf(q) === 0) score = 60;
      else if (words.length > 1 && words[words.length - 1] === code && haystack(a).indexOf(words[0]) >= 0) score = 90; // "Madrid (MAD)" typed back
      else if (haystack(a).indexOf(q) >= 0) score = 50;
      else if (words.length > 1 && words.every(function (w) { return haystack(a).indexOf(w) >= 0; })) score = 40;
      var home = LANG === "en" ? (a[3] === "ES" || UK[a[3]]) : a[3] === "ES";
      if (score >= 0) out.push([score + (home ? 5 : 0) + (a[6] ? 2 : 0), a]);
    }
    out.sort(function (x, y) { return y[0] - x[0] || (x[1][0] < y[1][0] ? -1 : 1); });
    return out.slice(0, 8).map(function (x) { return x[1]; });
  }
  window.CTT_search = function (q, data) { airports = data; return search(q); }; // exposed for tests

  function attach(input) {
    var list = document.getElementById(input.getAttribute("aria-controls"));
    var items = [], active = -1, sayT = null;
    // Screen readers: announce the number of results or the message (the list itself only holds options)
    var st = document.createElement("span"); st.className = "sr"; st.setAttribute("role", "status"); st.id = input.id + "-st";
    input.parentNode.appendChild(st);
    function say(text) { clearTimeout(sayT); sayT = setTimeout(function () { st.textContent = text; }, 450); }
    // Visible error under the field, linked with aria-describedby
    var err = document.createElement("p"); err.className = "field-err"; err.id = input.id + "-err"; err.hidden = true;
    input.parentNode.appendChild(err);
    function invalid(text) {
      if (text) { err.textContent = text; err.hidden = false; input.setAttribute("aria-invalid", "true"); input.setAttribute("aria-describedby", err.id); }
      else { err.hidden = true; input.removeAttribute("aria-invalid"); input.removeAttribute("aria-describedby"); }
    }
    function close() { list.hidden = true; input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant"); active = -1; }
    function pick(a) { input.value = label(a); input.dataset.code = a[0]; invalid(""); close(); run(); }
    function message(text) {
      list.innerHTML = ""; items = [];
      var li = document.createElement("li"); li.className = "ac-msg"; li.setAttribute("role", "option"); li.setAttribute("aria-disabled", "true"); li.textContent = text;
      list.appendChild(li); list.hidden = false; input.setAttribute("aria-expanded", "false"); say(text);
    }
    function render() {
      if (!input.value.trim()) { close(); return; }
      if (loadState === "loading") { message(T.acLoading); return; }
      if (loadState === "error") { message(T.acError); return; }
      items = search(input.value); active = -1;
      if (!items.length) { message(T.acNone); return; }
      list.innerHTML = "";
      items.forEach(function (a, i) {
        var li = document.createElement("li");
        li.id = input.id + "-opt-" + i;
        li.setAttribute("role", "option");
        li.setAttribute("aria-selected", "false");
        li.innerHTML = '<span class="opt-code"></span><span class="opt-txt"><b></b><small></small></span>';
        li.querySelector(".opt-code").textContent = a[0];
        li.querySelector("b").textContent = cityOf(a);
        li.querySelector("small").textContent = a[1] + (a[3] ? " · " + a[3] : "");
        // mousedown keeps the focus in the input (also fired after a tap); click is the fallback
        li.addEventListener("mousedown", function (e) { e.preventDefault(); pick(a); });
        li.addEventListener("click", function () { if (input.dataset.code !== a[0]) pick(a); });
        list.appendChild(li);
      });
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
      say(T.acCount(items.length));
    }
    function highlight() {
      Array.prototype.forEach.call(list.children, function (li, i) { li.classList.toggle("on", i === active); li.setAttribute("aria-selected", i === active ? "true" : "false"); });
      if (active >= 0) { input.setAttribute("aria-activedescendant", input.id + "-opt-" + active); var el = list.children[active]; if (el && el.scrollIntoView) el.scrollIntoView({ block: "nearest" }); }
    }
    // Leaving the field with an unambiguous text (exact code or a single match) selects it
    function autoPick() {
      if (input.dataset.code || loadState !== "ready" || !input.value.trim()) return;
      var r = search(input.value), q = norm(input.value.trim());
      if (r.length && (r[0][0].toLowerCase() === q || r.length === 1)) pick(r[0]);
      else { invalid(r.length ? T.pick : T.acNone); run(); }
    }
    input.addEventListener("input", function () { input.dataset.code = ""; invalid(""); render(); run(); });
    input.addEventListener("focus", function () { if (!input.dataset.code) render(); else input.select(); });
    input.addEventListener("blur", function () { setTimeout(function () { close(); autoPick(); }, 150); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" && list.hidden) { render(); if (items.length) { active = 0; highlight(); } e.preventDefault(); return; }
      if (list.hidden || !items.length) { if (e.key === "Escape") close(); return; }
      if (e.key === "ArrowDown") { active = Math.min(active + 1, items.length - 1); highlight(); e.preventDefault(); }
      else if (e.key === "ArrowUp") { active = Math.max(active - 1, 0); highlight(); e.preventDefault(); }
      else if (e.key === "Enter") { pick(items[active >= 0 ? active : 0]); e.preventDefault(); }
      else if (e.key === "Tab" && active >= 0) pick(items[active]);
      else if (e.key === "Escape") { close(); e.preventDefault(); }
    });
    input._render = render;
  }

  // ---------- Form wiring ----------
  var form, out;
  var AESA_CLAIM = "https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa";
  function val(name) { var el = form.querySelector('[name="' + name + '"]:checked') || form.querySelector('select[name="' + name + '"]'); return el ? el.value : ""; }
  function show(id, on) { var el = form.querySelector("#" + id); if (el) el.hidden = !on; }
  function syncVisibility() {
    var what = val("what"), notice = val("notice"), reroute = val("reroute"), denied = val("denied");
    var shortNotice = what === "cancel" && (notice === "7to14" || notice === "lt7");
    var alt = shortNotice && reroute === "yes";
    show("grp-delay", what === "delay");
    show("grp-notice", what === "cancel");
    show("grp-reroute", shortNotice);
    show("grp-rdep", alt); show("grp-rarr", alt); show("grp-accepted", alt);
    show("grp-denied", what === "denied");
    show("grp-checkin", what === "denied" && denied !== "vol");
    show("grp-dreason", what === "denied" && denied !== "vol");
    show("grp-cause", what !== "denied");
  }
  function inputs() {
    return { what: val("what"), delay: val("delay"), notice: val("notice"), reroute: val("reroute"), rdep: val("rdep"),
      rarr: val("rarr"), accepted: val("accepted"), denied: val("denied"), checkin: val("checkin"), dreason: val("dreason"), cause: val("cause"),
      via: val("via") || "direct", fare: val("fare") || "public" };
  }
  var touched = false, started = false, resTimer = null, lastSig = "";
  function resultParams(r, o) {
    return { incident_type: o.what, result: r.verdict, regime: r.regime || "none",
      compensation_category: r.verdict === "no" ? "none" : r.amount + "_" + r.cur };
  }
  // One calculator_completed (plus its result event) per distinct result, once the visitor stops changing answers
  function reportResult(r, o) {
    clearTimeout(resTimer);
    resTimer = setTimeout(function () {
      var p = resultParams(r, o), sig = [p.incident_type, p.result, p.compensation_category, p.regime].join("|");
      if (sig === lastSig) return;
      lastSig = sig;
      track("calculator_completed", p);
      track(r.verdict === "posible" ? "compensation_possible" : r.verdict === "insuficiente" ? "compensation_insufficient_data" : "compensation_not_eligible", p);
    }, 1200);
  }
  var emptyDefault = null;
  function emptyMsg(text) {
    var p = out.querySelector(".empty-msg"); if (!p) return;
    if (emptyDefault === null) emptyDefault = p.textContent;
    p.textContent = text || emptyDefault;
  }
  function run() {
    syncVisibility();
    var dep = byCode[form.querySelector("#from").dataset.code];
    var arr = byCode[form.querySelector("#to").dataset.code];
    if (loadState !== "ready" && !(dep && arr)) return;
    if (!dep || !arr || dep === arr) {
      var fromTxt = form.querySelector("#from").value.trim(), toTxt = form.querySelector("#to").value.trim();
      emptyMsg(dep && arr ? T.same : ((!dep && fromTxt) || (!arr && toTxt)) ? T.pick : null);
      out.dataset.state = "empty"; var cb = out.querySelector("[data-care]"); if (cb) cb.hidden = true; var wb = out.querySelector("[data-where]"); if (wb) wb.hidden = true; return;
    }
    var slug = val("airline");
    var al = AIRLINES.filter(function (x) { return x.slug === slug; })[0] || { eu: slug === "otra-ue" ? "yes" : slug === "otra-no-ue" ? "no" : "unknown" };
    var o = inputs(); o.dep = dep; o.arr = arr; o.airline = al;
    var r = compute(o);
    out.dataset.state = r.verdict;
    out.querySelector("[data-route]").textContent = dep[0] + " → " + arr[0];
    out.querySelector("[data-km]").textContent = fmt(r.dist || 0) + " km";
    out.querySelector("[data-amount]").textContent = money(r.amount || 0, r.cur);
    out.querySelector("[data-headline]").textContent =
      r.verdict === "posible" ? T.hPos(money(r.amount, r.cur)) : r.verdict === "insuficiente" ? T.hIns : T.hNo;
    var ul = out.querySelector("[data-lines]"); ul.innerHTML = "";
    function li(text, cls) { var x = document.createElement("li"); x.textContent = text; if (cls) x.className = cls; ul.appendChild(x); }
    r.missing.forEach(function (m) { li(T.missing + m, "missing"); });
    r.lines.forEach(function (t) { li(t); });
    r.notes.forEach(function (t) { li(t, "note"); });
    if (r.verdict === "insuficiente") li(T.letterLater, "note");
    care(r, o.what);
    where(al, r, dep, arr);
    // The claims-company link is shown whenever money could be owed, including when the airline must still prove an exemption.
    out.querySelector("[data-cta]").hidden = !(r.amount || r.potential);
    var lo = document.getElementById("letter-open"); if (lo) lo.hidden = r.verdict !== "posible";
    if (r.verdict !== "posible") { var lp = document.getElementById("letter"); if (lp) { lp.hidden = true; if (lo) lo.setAttribute("aria-expanded", "false"); } }
    var alName = (form.querySelector("#airline").selectedOptions[0] || {}).textContent || "";
    last = { r: r, dep: dep, arr: arr, o: o, airline: (slug && slug.indexOf("otra") !== 0) ? alName : "" };
    letter();
    if (touched) reportResult(r, o);
  }

  // ---------- Right to care (Art. 6, 8, 9) ----------
  function care(r, what) {
    var box = out.querySelector("[data-care]"); if (!box) return;
    if (r.covered === false || !r.regime) { box.hidden = true; return; }
    var en = LANG === "en", dist = r.dist || 0, items;
    var h = dist <= 1500 ? 2 : (r.intra || dist <= 3500) ? 3 : 4; // Art. 6(1): 2 h / 3 h (incl. intra-EU >1,500 km) / 4 h
    if (what === "delay") {
      items = en ? [
        "Meals and drinks if your flight leaves " + h + "+ hours late (for this distance).",
        "A hotel and transfers if the new departure is the next day.",
        "Delayed 5+ hours? You can give up the trip and get a full refund."
      ] : [
        "Comida y bebida si el vuelo sale con " + h + " h o más de retraso (para esta distancia).",
        "Hotel y traslados si la salida se pasa al día siguiente.",
        "¿Más de 5 h de retraso? Puedes renunciar al viaje y pedir el reembolso completo."
      ];
    } else {
      items = en ? [
        "Your choice of a full refund within 7 days or a new flight.",
        "Meals and drinks while you wait for the new flight.",
        "A hotel and transfers if you have to stay overnight."
      ] : [
        "A tu elección: reembolso completo en 7 días o un vuelo alternativo.",
        "Comida y bebida mientras esperas el vuelo alternativo.",
        "Hotel y traslados si tienes que pasar la noche."
      ];
    }
    var head = en ? "Whatever the result, while you wait you're owed:" : "Sea cual sea el resultado, mientras esperas te deben:";
    var tip = en ? "Didn't get it and paid yourself? Keep the receipts: the airline must pay you back, even if the cause was extraordinary."
      : "¿No te lo dieron y lo pagaste tú? Guarda los tickets: la aerolínea tiene que devolvértelo, aunque la causa sea extraordinaria.";
    box.innerHTML = "<h3></h3><ul></ul><p class=\"tip\"></p>";
    box.querySelector("h3").textContent = head;
    items.forEach(function (t) { var li = document.createElement("li"); li.textContent = t; box.querySelector("ul").appendChild(li); });
    box.querySelector(".tip").textContent = tip;
    box.hidden = false;
  }

  // ---------- Where to claim (official airline channel + escalation) ----------
  // EU261: the enforcement body of the departure country, or of the arrival country for flights from outside the EU (Art. 16).
  function nebCountry(r, dep, arr) { return r.regime === "UK" ? "UK" : (dep[6] === 1 ? dep[3] : arr[3]); }
  function where(al, r, dep, arr) {
    var box = out.querySelector("[data-where]"); if (!box) return;
    var en = LANG === "en", h = "", name = al && al.name;
    if (name && al.claim) {
      h += "<p><strong>" + (en ? "Claim from " + name + " for free: " : "Reclama gratis a " + name + ": ") + "</strong>" +
        '<a href="' + al.claim + '" rel="noopener nofollow" target="_blank">' + (en ? "official claim page" : "página oficial de reclamación") + "</a>.</p>";
      if (al.note) h += "<p>" + al.note.replace(/</g, "&lt;") + "</p>";
    }
    var esc, nc = nebCountry(r, dep, arr);
    if (nc === "UK") {
      var adr = al && al.adr;
      esc = en ? "If they refuse or don't reply in 8 weeks: " + (adr && adr !== "CAA" ? adr + " (the airline's free dispute scheme)" : "the CAA's free complaints service (PACT)") + "."
        : "Si lo rechazan o no contestan en 8 semanas: " + (adr && adr !== "CAA" ? adr + " (mediación gratuita)" : "el servicio de reclamaciones de la CAA, gratuito") + ".";
    } else if (nc === "ES") {
      esc = (en ? "If they refuse or don't reply within a month: " : "Si lo rechazan o no contestan en un mes: ") +
        '<a href="' + AESA_CLAIM + '" rel="noopener" target="_blank">' + (en ? "AESA, Spain's aviation authority (free)" : "reclama a AESA, gratis") + "</a>.";
    } else {
      esc = en ? "If they refuse or don't reply: the national enforcement body of the " + (dep[6] === 1 ? "departure" : "arrival") + " country (free)."
        : "Si lo rechazan o no contestan: el organismo nacional de aviación del país de " + (dep[6] === 1 ? "salida" : "llegada") + ", gratis.";
    }
    h += "<p class=\"tip\">" + esc + "</p>";
    box.innerHTML = "<h3>" + (en ? "Where to claim" : "Dónde reclamar") + "</h3>" + h;
    box.hidden = r.verdict === "no" && !r.potential;
  }

  // ---------- Claim letter (runs only in the browser; only for "posible") ----------
  var last = null;
  function fval(id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; }
  function fdate(iso, ph) {
    if (!iso) return ph;
    var p = iso.split("-"); return p[2] + "/" + p[1] + "/" + p[0];
  }
  // The letter is only offered for the "posible" result. It states the passenger's position and asks the airline to pay
  // or to prove an exemption; it never claims that the right is already established. No bank details are requested.
  var CAUSE_L = {
    es: {
      unknown: "La compañía no me comunicó el motivo.",
      tech: "Se me indicó que el motivo fue un problema técnico, que según el Tribunal de Justicia de la UE no constituye por sí solo una circunstancia extraordinaria (asunto C-549/07).",
      crew: "Se me indicó que el motivo fue la falta o indisposición de la tripulación, que no constituye una circunstancia extraordinaria (asuntos C-156/22 a C-158/22).",
      strike_own: "Se me indicó que el motivo fue una huelga del personal de la propia compañía, que no constituye una circunstancia extraordinaria (asunto C-28/20)."
    },
    en: {
      unknown: "The airline did not tell me the reason.",
      tech: "I was told the reason was a technical problem, which according to the Court of Justice of the EU is not in itself an extraordinary circumstance (Case C-549/07).",
      crew: "I was told the reason was a crew shortage or illness, which is not an extraordinary circumstance (Cases C-156/22 to C-158/22).",
      strike_own: "I was told the reason was a strike by the airline's own staff, which is not an extraordinary circumstance (Case C-28/20)."
    }
  };
  function cancelFacts(o, en) {
    var n = o.notice === "7to14" ? (en ? "between 7 and 13 days" : "entre 7 y 13 días") : (en ? "less than 7 days" : "menos de 7 días");
    var s = en ? "The flight was cancelled and I was informed " + n + " before departure. " : "El vuelo fue cancelado y se me informó con " + n + " de antelación. ";
    if (o.reroute === "no") return s + (en ? "I was not offered alternative transport." : "No se me ofreció un transporte alternativo.");
    var dep = { le1: en ? "no more than 1 hour earlier than, or after," : "como mucho 1 hora antes que el original, o después de él,", "1to2": en ? "between 1 and 2 hours earlier than" : "entre 1 y 2 horas antes que el original", gt2: en ? "more than 2 hours earlier than" : "más de 2 horas antes que el original" }[o.rdep];
    var arr = { lt2: en ? "less than 2 hours after" : "menos de 2 horas después que el original", "2to4": en ? "between 2 and 4 hours after" : "entre 2 y 4 horas después que el original", ge4: en ? "4 or more hours after" : "4 horas o más después que el original" }[o.rarr];
    var acc = o.accepted === "yes" ? (en ? " I accepted it." : " Lo acepté.") : o.accepted === "no" ? (en ? " I did not accept it and requested a refund." : " No lo acepté y solicité el reembolso.") : "";
    return s + (en ? "The alternative flight offered left " + dep + " the original and arrived " + arr + " the original, outside the limits of Article 5(1)(c)." + acc
      : "El vuelo alternativo ofrecido salía " + dep + " y llegaba " + arr + ", fuera de los márgenes del artículo 5.1.c)." + acc);
  }
  function letterFacts(L, en) {
    var o = L.o, f;
    if (o.what === "delay") {
      f = en ? "The flight arrived at its final destination " + (o.delay === "3to4" ? "between 3 and 4 hours" : "more than 4 hours") + " late."
        : "El vuelo llegó a su destino final con un retraso " + (o.delay === "3to4" ? "de entre 3 y 4 horas" : "de más de 4 horas") + ".";
    } else if (o.what === "cancel") f = cancelFacts(o, en);
    else {
      f = en ? "I was denied boarding against my will, although I checked in and presented myself for boarding on time with valid travel documents."
        : "Se me denegó el embarque contra mi voluntad, a pesar de presentarme a tiempo a la facturación y al embarque con la documentación en regla.";
      if (o.dreason === "overbooking") f += en ? " The airline gave overbooking or another operational reason." : " La compañía alegó overbooking u otro motivo operativo.";
      else f += en ? " I was not given any reason of health, safety, security or travel documents." : " No se me indicó ningún motivo de salud, seguridad o documentación.";
    }
    if (o.what !== "denied") { var c = { strike: "strike_own" }[o.cause] || o.cause; f += " " + (CAUSE_L[en ? "en" : "es"][c] || CAUSE_L[en ? "en" : "es"].unknown); }
    return f;
  }
  function letterES(L, d) {
    var o = L.o, legal;
    if (o.what === "delay") legal = "los artículos 6 y 7 del Reglamento (CE) n.º 261/2004 y la sentencia del Tribunal de Justicia de la UE de 19 de noviembre de 2009 (asuntos C-402/07 y C-432/07, Sturgeon), que reconoce el derecho a compensación a partir de 3 horas de retraso en la llegada";
    else if (o.what === "cancel") legal = "los artículos 5 y 7 del Reglamento (CE) n.º 261/2004";
    else legal = "los artículos 4 y 7 del Reglamento (CE) n.º 261/2004";
    var uk = L.r.regime === "UK";
    if (uk) legal = legal.replace("Reglamento (CE) n.º 261/2004", "Reglamento (CE) n.º 261/2004 en su versión vigente en el Reino Unido (UK261)");
    var nc = nebCountry(L.r, L.dep, L.arr);
    var neb = uk ? "la Autoridad de Aviación Civil del Reino Unido (CAA) o el organismo de resolución de conflictos de la aerolínea"
      : nc === "ES" ? "la Agencia Estatal de Seguridad Aérea (AESA)" : "el organismo nacional competente en materia de derechos de los pasajeros";
    var n = d.n, amt = money(L.r.amount, L.r.cur);
    var reduced = L.r.amount < L.r.full;
    return "Asunto: Reclamación de compensación, vuelo " + d.flight + " del " + d.date + "\n\n" +
      "A la atención de " + (L.airline || "[aerolínea]") + ", servicio de atención al cliente:\n\n" +
      "Yo, " + d.name + ", viajé " + (n > 1 ? "junto con " + (n - 1) + " pasajero" + (n > 2 ? "s" : "") + " más " : "") +
      "con la reserva " + d.booking + " en el vuelo " + d.flight + " del " + d.date + ", de " + d.route + ".\n\n" +
      letterFacts(L, false) + "\n\n" +
      "Considero que, de acuerdo con " + legal + ", tengo derecho a una compensación de " + amt + " por pasajero" +
      (n > 1 ? " (" + money(L.r.amount * n, L.r.cur) + " en total por " + n + " pasajeros)" : "") +
      ", correspondiente a un vuelo de " + fmt(L.r.dist) + " km" + (reduced ? ", importe ya reducido conforme al artículo 7.2" : "") + ", y les solicito su abono.\n\n" +
      "Si consideran que concurre una circunstancia extraordinaria que no pudo evitarse aun adoptando todas las medidas razonables, les ruego que me indiquen cuál fue y me faciliten la documentación que lo acredite.\n\n" +
      "Les ruego que, en un plazo de 30 días, me indiquen cómo y cuándo abonarán la compensación. Les recuerdo que debe pagarse en metálico, por transferencia o por cheque, y que solo aceptaré bonos u otros servicios si lo acuerdo por escrito (artículo 7.3).\n\n" +
      "Si no recibo una respuesta satisfactoria, presentaré la reclamación ante " + neb + " y, en su caso, ante los tribunales.\n\n" +
      "Adjunto la tarjeta de embarque y la confirmación de la reserva.\n\n" +
      "Atentamente,\n" + d.name + "\n" + d.today + "\n";
  }
  function letterEN(L, d) {
    var o = L.o, legal;
    if (o.what === "delay") legal = "Articles 6 and 7 of Regulation (EC) No 261/2004 and the judgment of the Court of Justice of the EU of 19 November 2009 (Joined Cases C-402/07 and C-432/07, Sturgeon), which recognises the right to compensation for arrival delays of 3 hours or more";
    else if (o.what === "cancel") legal = "Articles 5 and 7 of Regulation (EC) No 261/2004";
    else legal = "Articles 4 and 7 of Regulation (EC) No 261/2004";
    var uk = L.r.regime === "UK";
    if (uk) legal = legal.replace("Regulation (EC) No 261/2004", "Regulation (EC) No 261/2004 as retained in UK law (UK261)");
    var nc = nebCountry(L.r, L.dep, L.arr);
    var neb = uk ? "the UK Civil Aviation Authority (CAA) or the airline's approved ADR scheme"
      : nc === "ES" ? "Spain's aviation safety agency (AESA)" : "the competent national enforcement body";
    var n = d.n, amt = money(L.r.amount, L.r.cur);
    var reduced = L.r.amount < L.r.full;
    return "Subject: Compensation claim, flight " + d.flight + " on " + d.date + "\n\n" +
      "To " + (L.airline || "[airline]") + " customer services,\n\n" +
      "I, " + d.name + ", travelled " + (n > 1 ? "with " + (n - 1) + " other passenger" + (n > 2 ? "s" : "") + " " : "") +
      "under booking " + d.booking + " on flight " + d.flight + " on " + d.date + ", from " + d.route + ".\n\n" +
      letterFacts(L, true) + "\n\n" +
      "I consider that, under " + legal + ", I am entitled to compensation of " + amt + " per passenger" +
      (n > 1 ? " (" + money(L.r.amount * n, L.r.cur) + " in total for " + n + " passengers)" : "") +
      ", corresponding to a flight distance of " + fmt(L.r.dist) + " km" + (reduced ? ", already reduced under Article 7(2)" : "") + ", and I ask you to pay it.\n\n" +
      "If you consider that extraordinary circumstances applied which could not have been avoided even if all reasonable measures had been taken, please tell me what they were and provide the supporting evidence.\n\n" +
      "Please let me know within 30 days how and when you will pay the compensation. It must be paid in cash, by bank transfer or by cheque; I will only accept vouchers or other services if I agree to it in writing (Article 7(3)).\n\n" +
      "If I do not receive a satisfactory reply, I will refer the claim to " + neb + " and, if necessary, to the courts.\n\n" +
      "Please find attached my boarding pass and booking confirmation.\n\n" +
      "Yours faithfully,\n" + d.name + "\n" + d.today + "\n";
  }
  function letter() {
    var box = document.getElementById("letter-text");
    if (!box || !last) return;
    if (last.r.verdict !== "posible" || !last.r.amount) { box.value = ""; return; }
    var L = last, en = LANG === "en";
    var today = new Date();
    var d = {
      n: Math.max(1, Math.min(9, parseInt(fval("l-pax"), 10) || 1)),
      name: fval("l-name") || (en ? "[your full name]" : "[tu nombre y apellidos]"),
      flight: fval("l-flight").toUpperCase() || (en ? "[flight number]" : "[número de vuelo]"),
      booking: fval("l-booking").toUpperCase() || (en ? "[booking reference]" : "[código de reserva]"),
      date: fdate(fval("l-date"), en ? "[flight date]" : "[fecha del vuelo]"),
      route: cityOf(L.dep) + " (" + L.dep[0] + ")" + (en ? " to " : " a ") + cityOf(L.arr) + " (" + L.arr[0] + ")",
      today: ("0" + today.getDate()).slice(-2) + "/" + ("0" + (today.getMonth() + 1)).slice(-2) + "/" + today.getFullYear()
    };
    box.value = en ? letterEN(L, d) : letterES(L, d);
  }
  window.CTT_letters = { es: letterES, en: letterEN }; // exposed for tests
  function letterTools() {
    var panel = document.getElementById("letter");
    if (!panel) return;
    panel.addEventListener("input", letter);
    var copy = document.getElementById("letter-copy"), dl = document.getElementById("letter-dl"), msg = document.getElementById("letter-msg");
    copy.addEventListener("click", function () {
      var t = document.getElementById("letter-text");
      function sel() { t.focus(); t.select(); msg.textContent = T.selected; }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t.value).then(function () { msg.textContent = T.copied; track("letter_copied", last ? resultParams(last.r, last.o) : {}); }, sel);
      } else sel();
    });
    dl.addEventListener("click", function () {
      try {
        var blob = new Blob([document.getElementById("letter-text").value], { type: "text/plain;charset=utf-8" });
        var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = T.file;
        document.body.appendChild(a); a.click(); a.remove();
        msg.textContent = T.downloaded;
        track("letter_downloaded", last ? resultParams(last.r, last.o) : {});
      } catch (e) { msg.textContent = T.dlFail; }
    });
    var open = document.getElementById("letter-open");
    open.addEventListener("click", function () {
      panel.hidden = !panel.hidden; open.setAttribute("aria-expanded", String(!panel.hidden));
      if (!panel.hidden) { letter(); document.getElementById("l-name").focus(); track("letter_opened", last ? resultParams(last.r, last.o) : {}); }
    });
  }

  function markScrollables() {
    if (!document.querySelectorAll) return; // test harness without DOM
    Array.prototype.forEach.call(document.querySelectorAll(".board"), function (el) {
      if (el.scrollWidth > el.clientWidth + 1) {
        var h = el.previousElementSibling, k = 0;
        while (h && !/^H[2-4]$/.test(h.tagName) && k++ < 4) h = h.previousElementSibling;
        if (!h || !/^H[2-4]$/.test(h.tagName)) { var sec = el.closest("section, .wrap"); h = sec && sec.querySelector("h2, h3"); }
        el.setAttribute("tabindex", "0"); el.setAttribute("role", "region");
        el.setAttribute("aria-label", (h ? h.textContent.trim() + " (" : "") + T.tableScroll + (h ? ")" : ""));
      } else if (el.getAttribute("role") === "region") { el.removeAttribute("tabindex"); el.removeAttribute("role"); el.removeAttribute("aria-label"); }
    });
  }
  var msT = null;
  function init() {
    if (window.addEventListener) window.addEventListener("resize", function () { clearTimeout(msT); msT = setTimeout(markScrollables, 200); });
    markScrollables();
    // Clicks on affiliate links anywhere on the site (calculator button, comparison page...)
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[rel~="sponsored"]');
      if (!a) return;
      var p = last ? resultParams(last.r, last.o) : {};
      p.affiliate_id = affId(a.href);
      p.placement = a.closest("[data-cta]") ? "calculator" : "content";
      track("affiliate_click", p);
    }, true);
    form = document.getElementById("calc");
    out = document.getElementById("result");
    if (!form) return;
    function touch(e) {
      if (e.target.closest && e.target.closest("#letter")) return;
      touched = true;
      if (!started) started = track("calculator_started", { incident_type: val("what") }); // sent once consent exists
    }
    form.addEventListener("input", touch, true);
    form.addEventListener("change", touch, true);
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    form.addEventListener("change", function (e) { if (!e.target.closest || !e.target.closest("#letter")) run(); });
    letterTools();
    // Blogs embedding the calculator may use their own affiliate link (known claims domains only)
    try {
      var aff = new URLSearchParams(location.search).get("aff");
      if (aff) {
        var u = new URL(aff), ok = /(^|\.)(airhelp\.com|airadvisor\.com|compensair\.com|flightright\.(es|com|de|co\.uk)|skyrefund\.com|reclamador\.es|tp\.media|travelpayouts\.com|postaffiliatepro\.com)$/.test(u.hostname);
        if (u.protocol === "https:" && ok) {
          var a = out.querySelector("[data-cta] a.btn-sign"), sm = out.querySelector("[data-cta] small[data-generic]");
          if (a) { a.href = u.href; if (a.dataset.generic) a.textContent = a.dataset.generic; } // another provider: no AirHelp-specific claims
          if (sm && sm.firstChild) sm.firstChild.nodeValue = sm.dataset.generic + " ";
        }
      }
    } catch (err) { /* invalid parameter: keep the default link */ }
    ["from", "to"].forEach(function (id) { attach(document.getElementById(id)); });
    var retry = document.getElementById("ac-retry");
    if (retry) retry.addEventListener("click", function () { loadAirports(0); });
    window.addEventListener("online", function () { if (loadState === "error") loadAirports(0); });
    // The example route is computed with the airports embedded in the page; the full list (about 90 KB) is
    // downloaded as soon as the visitor touches an airport field, or once the page has finished loading.
    (cfg.seed || []).forEach(function (a) { byCode[a[0]] = a; });
    ["from", "to"].forEach(function (id) { var el = document.getElementById(id), a = byCode[el.dataset.code]; if (a) el.value = label(a); });
    var seeded = !!(byCode[document.getElementById("from").dataset.code] && byCode[document.getElementById("to").dataset.code]);
    if (!seeded) { loadAirports(0); return; }
    run();
    var started_ = false;
    function startLoad() { if (started_) return; started_ = true; loadAirports(0); }
    ["from", "to"].forEach(function (id) { var el = document.getElementById(id); el.addEventListener("focus", startLoad); el.addEventListener("pointerdown", startLoad); });
    if (document.readyState === "complete") setTimeout(startLoad, 1200);
    else window.addEventListener("load", function () { setTimeout(startLoad, 1200); });
  }
  // Airport list: 15 s timeout, one automatic retry, HTTP and format checks, then a visible error with a retry button.
  function loadAirports(attempt) {
    loadState = "loading";
    if (out.dataset.state === "empty" || out.dataset.state === "error") { out.dataset.state = "empty"; emptyMsg(T.loading); }
    var ctrl = typeof AbortController === "function" ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
    fetch(cfg.dataUrl, ctrl ? { signal: ctrl.signal } : undefined).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    }).then(function (d) {
      clearTimeout(timer);
      if (!Array.isArray(d) || d.length < 100 || !Array.isArray(d[0]) || d[0].length < 7) throw new Error("formato");
      airports = d; byCode = {}; d.forEach(function (a) { byCode[a[0]] = a; });
      loadState = "ready"; emptyMsg(null);
      ["from", "to"].forEach(function (id) {
        var el = document.getElementById(id), a = byCode[el.dataset.code];
        if (a) el.value = label(a);
        else if (el.value.trim() && document.activeElement === el && el._render) el._render(); // typed while loading
      });
      run();
    }).catch(function () {
      clearTimeout(timer);
      if (attempt < 1) { setTimeout(function () { loadAirports(attempt + 1); }, 1500); return; }
      loadState = "error"; out.dataset.state = "error";
      var m = out.querySelector(".error-msg [data-error-text]");
      if (m) m.textContent = navigator.onLine === false ? T.offline : T.loadError;
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
