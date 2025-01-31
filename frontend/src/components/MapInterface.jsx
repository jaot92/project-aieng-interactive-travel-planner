import { MapContainer, TileLayer, Marker } from 'react-leaflet'

const MapView = ({ locations }) => (
  <MapContainer center={[18.2208, -66.5901]} zoom={9}>
    <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
    {locations.map((loc, i) => (
      <Marker key={i} position={[loc.lat, loc.lng]}>
        <Popup>{loc.name}</Popup>
      </Marker>
    ))}
  </MapContainer>
) 