import request from '@/utils/request'

export const checkRooms = data =>
  request.post('/api/reservations/check/', data)

export const createReservation = data =>
  request.post('/api/reservations/create/', data)

export const getMyReservations = () =>
  request.get('/api/reservations/my/')

export const cancelReservation = id =>
  request.post(`/api/reservations/${id}/cancel`)

export const confirmUse = id =>
  request.post(`/api/reservations/${id}/confirm`)
