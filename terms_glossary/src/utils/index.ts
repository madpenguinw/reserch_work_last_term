export const parseJsonSafely = (stringJson: any) => {
  try {
    return JSON.parse(stringJson) as object
  } catch {
    return null
  }
}
