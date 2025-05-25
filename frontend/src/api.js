export async function getWyniki() {
  const res = await fetch('/api/wyniki');
  return await res.json();
}
export async function getZawodnicy() {
  const res = await fetch('/api/zawodnicy');
  return await res.json();
}
export async function getKategorie() {
  const res = await fetch('/api/kategorie');
  return await res.json();
}
export async function getDrabinka() {
  const res = await fetch('/api/drabinka');
  return await res.json();
}

