package handler

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
)

type Product struct {
	ID    string  `json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

type ProductHandler struct {
	products map[string]Product
}

func NewProductHandler() *ProductHandler {
	return &ProductHandler{
		products: map[string]Product{
			"1": {ID: "1", Name: "Laptop", Price: 15000000},
			"2": {ID: "2", Name: "Mouse", Price: 250000},
			"3": {ID: "3", Name: "Keyboard", Price: 750000},
		},
	}
}

func (h *ProductHandler) Health(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (h *ProductHandler) ListProducts(w http.ResponseWriter, r *http.Request) {
	list := make([]Product, 0, len(h.products))
	for _, p := range h.products {
		list = append(list, p)
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *ProductHandler) GetProduct(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")
	p, ok := h.products[id]
	if !ok {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "product not found"})
		return
	}
	writeJSON(w, http.StatusOK, p)
}

func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(data)
}
