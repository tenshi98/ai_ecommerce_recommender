/**
 * @file Lógica de la interfaz de AI E-Commerce Product Recommender.
 *
 * Toda la comunicación con el backend se realiza con `fetch`. Las respuestas
 * del modelo se insertan en el DOM mediante `textContent` o creando nodos,
 * nunca con `innerHTML`, para evitar inyección de HTML.
 */

"use strict";

/**
 * Muestra un mensaje de error dentro de un contenedor.
 *
 * @param {HTMLElement} container - Elemento donde se mostrará el mensaje.
 * @param {string} message - Texto del error.
 * @returns {void}
 */
function showError(container, message) {
    container.replaceChildren();
    const paragraph = document.createElement("p");
    paragraph.className = "error-message";
    paragraph.textContent = message;
    container.appendChild(paragraph);
}

/**
 * Sustituye el contenido de un contenedor por un párrafo de texto plano.
 *
 * @param {HTMLElement} container - Elemento que se actualizará.
 * @param {string} text - Texto a mostrar.
 * @returns {void}
 */
function setParagraph(container, text) {
    container.replaceChildren();
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    container.appendChild(paragraph);
}

/** Área de texto con las preferencias de compra. */
const preferencesInput = document.getElementById("preferences");
/** Botón que solicita las recomendaciones. */
const recommendButton = document.getElementById("recommend-button");
/** Contenedor de las recomendaciones. */
const responseDiv = document.getElementById("response");

/**
 * Envía las preferencias y muestra los productos recomendados.
 *
 * @async
 * @function getRecommendations
 * @param {Event} event - Evento de clic del botón.
 * @returns {Promise<void>} No devuelve valor; actualiza el DOM.
 */
async function getRecommendations(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("preferences", preferencesInput.value);

    try {
        const response = await fetch("/recommend", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            showError(responseDiv, "Error: Unable to process the request.");
            return;
        }

        const data = await response.json();
        setParagraph(responseDiv, data.recommendations);
    } catch (error) {
        showError(responseDiv, "Error: Unable to process the request.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    recommendButton.addEventListener("click", getRecommendations);
});
