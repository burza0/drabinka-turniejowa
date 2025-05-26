import axios from 'axios'

export async function getDrabinka() {
  const res = await axios.get('/api/drabinka')
  return res.data
}

export async function getKategorie() {
  const res = await axios.get('/api/kategorie')
  return res.data
}

export async function getWyniki(kategoria) {
  // Jeśli backend pozwala filtrować po kategorii:
  if (kategoria)
    return (await axios.get('/api/wyniki?kategoria=' + encodeURIComponent(kategoria))).data
  // Jeśli nie, pobierz wszystkie:
  return (await axios.get('/api/wyniki')).data
}

