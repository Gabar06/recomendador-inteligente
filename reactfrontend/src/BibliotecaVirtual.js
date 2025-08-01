import React, { useEffect, useState } from 'react';

// Íconos SVG (puedes reemplazar por imágenes o librerías como react-icons)
const DownloadIcon = () => (
  <span role="img" aria-label="descargar">📥</span>
);
const EditIcon = () => (
  <span role="img" aria-label="editar">✏️</span>
);
const DeleteIcon = () => (
  <span role="img" aria-label="eliminar">🗑️</span>
);
const SearchIcon = () => (
  <svg height="25" width="25" viewBox="0 0 24 24" style={{verticalAlign: 'middle'}}><circle cx="11" cy="11" r="8" stroke="green" strokeWidth="2" fill="none"/><line x1="16" y1="16" x2="22" y2="22" stroke="purple" strokeWidth="2"/></svg>
);

function BibliotecaVirtual() {
  const [libros, setLibros] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [filtro, setFiltro] = useState([]);
  
  // Simulando fetch desde Django
  /*useEffect(() => {
    // Reemplaza esto por tu fetch real a la API de Django
    setLibros([
      {
        id: 1,
        titulo: "Manual de Reglas Ortográficas",
        autor: "InterWare de México, S.A. de C.V.",
        anio: 2022,
        editorial: "InterWare de México, S.A. de C.V.",
        archivo: "manual_reglas.pdf"
      }
      // ...más libros
    ]);
  }, []);*/
    useEffect(() => {
        fetch('http://localhost:8000/api/libros/')
          .then(res => res.json())
          .then(data => setLibros(data));
        }, []);
        //POST
        fetch('http://localhost:8000/api/libros/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({titulo, autor, editorial, año, archivo}),
        })
        .then(res => res.json())
        .then(data => { /* actualiza la lista o muestra mensaje */ });
        //PUT
        fetch(`http://localhost:8000/api/libros/${id}/`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({titulo, autor, editorial, año, archivo}),
        })
        .then(res => res.json())
        .then(data => { /* actualiza la lista o muestra mensaje */ });
        //DELETE
        fetch(`http://localhost:8000/api/libros/${id}/`, {
          method: 'DELETE',
        })
        .then(() => { /* actualiza la lista o muestra mensaje */ });

  useEffect(() => {
    setFiltro(
      libros.filter(libro =>
        libro.titulo.toLowerCase().includes(busqueda.toLowerCase()) ||
        libro.autor.toLowerCase().includes(busqueda.toLowerCase()) ||
        libro.editorial.toLowerCase().includes(busqueda.toLowerCase())
      )
    );
  }, [busqueda, libros]);

  return (
    <div style={{
      background: "#f6fff7",
      minHeight: "100vh",
      padding: "40px",
      fontFamily: "Inter, Arial, sans-serif"
    }}>
      <div style={{
        margin: "auto",
        maxWidth: 900,
        boxShadow: "0 0 16px 0 #57eb9640",
        borderRadius: 18,
        overflow: "hidden"
      }}>
        <div style={{ background: "#37D539", padding: "28px 0" }}>
          <h1 style={{
            textAlign: "center",
            color: "#fff",
            fontSize: "2.8rem",
            fontWeight: 700,
            margin: 0,
            letterSpacing: 1
          }}>Biblioteca Virtual</h1>
        </div>
        <div style={{
          background: "#fff",
          padding: 32,
          borderRadius: "0 0 18px 18px",
          boxShadow: "0 0 8px 0 #37D53918"
        }}>
          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap"
          }}>
            <div style={{
              flexGrow: 1,
              display: "flex",
              alignItems: "center",
              border: "2px solid #37D539",
              borderRadius: 32,
              overflow: "hidden",
              marginRight: 24
            }}>
              <input
                value={busqueda}
                onChange={e => setBusqueda(e.target.value)}
                placeholder="Buscar por título, autor o editorial..."
                style={{
                  border: "none",
                  outline: "none",
                  padding: "16px 24px",
                  fontSize: 18,
                  flex: 1
                }}
              />
              <button
                style={{
                  background: "#37D539",
                  border: "none",
                  padding: "0 28px",
                  height: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  cursor: "pointer",
                  borderRadius: "0 32px 32px 0"
                }}
                tabIndex={-1}
              >
                <SearchIcon />
              </button>
            </div>
            <button
              style={{
                background: "#37D539",
                color: "#fff",
                border: "none",
                borderRadius: 14,
                padding: "13px 28px",
                fontSize: 18,
                fontWeight: 600,
                cursor: "pointer",
                transition: "0.2s"
              }}
              onClick={() => alert("Aquí iría el modal para agregar un libro")}
            >
              + Agregar nuevo libro
            </button>
          </div>

          <table style={{
            width: "100%",
            marginTop: 38,
            borderCollapse: "collapse",
            fontSize: 17,
            background: "#f0fff0",
            borderRadius: 14,
            overflow: "hidden"
          }}>
            <thead>
              <tr style={{ background: "#d7ffd7" }}>
                <th style={thStyle}>Título</th>
                <th style={thStyle}>Autor</th>
                <th style={thStyle}>Año</th>
                <th style={thStyle}>Editorial</th>
                <th style={thStyle}>Archivo</th>
                <th style={thStyle}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtro.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: "center", padding: 20, color: "#aaa" }}>Sin resultados</td>
                </tr>
              ) : (
                filtro.map(libro => (
                  <tr key={libro.id} style={{ background: "#fff" }}>
                    <td style={tdStyle}>{libro.titulo}</td>
                    <td style={tdStyle}>{libro.autor}</td>
                    <td style={tdStyle}>{libro.anio}</td>
                    <td style={tdStyle}>{libro.editorial}</td>
                    <td style={tdStyle}>
                      <a href={libro.archivo} download style={{ textDecoration: "none" }}>
                        <DownloadIcon />
                      </a>
                    </td>
                    <td style={{ ...tdStyle, fontSize: 22 }}>
                      <span style={actionIconStyle} title="Editar" onClick={() => alert("Editar libro")}>
                        <EditIcon />
                      </span>
                      <span style={actionIconStyle} title="Eliminar" onClick={() => alert("Eliminar libro")}>
                        <DeleteIcon />
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// Estilos para celdas
const thStyle = {
  padding: "15px 10px",
  textAlign: "left",
  color: "#1a7f38",
  fontWeight: 700
};
const tdStyle = {
  padding: "13px 10px",
  verticalAlign: "middle",
};
const actionIconStyle = {
  cursor: "pointer",
  marginRight: 16,
  transition: "transform 0.13s",
  display: "inline-block",
  userSelect: "none"
};

export default BibliotecaVirtual;
