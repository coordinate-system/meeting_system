import request from '@/utils/request'

export const getRooms = () =>
  request.get('/api/rooms/list/')
