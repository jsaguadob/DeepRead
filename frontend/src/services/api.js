import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
};

export const readings = {
  list: (params) => api.get('/lecturas', { params }),
  get: (id) => api.get(`/lecturas/${id}`),
  create: (data) => api.post('/lecturas', data),
  update: (id, data) => api.put(`/lecturas/${id}`, data),
  delete: (id) => api.delete(`/lecturas/${id}`),
  complete: (id) => api.post(`/lecturas/${id}/completar`),
  importarArchivo: (formData) => api.post('/lecturas/importar-archivo', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
};

export const quizzes = {
  getQuestions: (lecturaId) => api.get(`/lecturas/${lecturaId}/preguntas`),
  createQuestion: (lecturaId, data) => api.post(`/lecturas/${lecturaId}/preguntas`, data),
  batchCreate: (lecturaId, data) => api.post(`/lecturas/${lecturaId}/preguntas/batch`, data),
  updateQuestion: (id, data) => api.put(`/preguntas/${id}`, data),
  deleteQuestion: (id) => api.delete(`/preguntas/${id}`),
  submitQuiz: (lecturaId, data) => api.post(`/lecturas/${lecturaId}/quiz/submit`, data),
};

export const groups = {
  list: () => api.get('/grupos'),
  get: (id) => api.get(`/grupos/${id}`),
  create: (data) => api.post('/grupos', data),
  join: (codigo) => api.post('/grupos/unirse', { codigo }),
  removeMember: (groupId, userId) => api.delete(`/grupos/${groupId}/miembros/${userId}`),
  getGrades: (groupId) => api.get(`/grupos/${groupId}/calificaciones`),
  toggleLecture: (groupId, lectureId, data) => api.post(`/grupos/${groupId}/cerrar_lectura/${lectureId}`, data),
  getLectureStatus: (groupId, lectureId) => api.get(`/grupos/${groupId}/estado_lectura/${lectureId}`),
};

export const activities = {
  list: () => api.get('/actividades'),
  get: (id) => api.get(`/actividades/${id}`),
  create: (data) => api.post('/actividades', data),
  submit: (id, data) => api.post(`/actividades/${id}/submit`, data),
  delete: (id) => api.delete(`/actividades/${id}`),
};

export const users = {
  list: () => api.get('/users'),
  update: (id, data) => api.put(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
};

export const institutions = {
  list: () => api.get('/instituciones'),
  create: (data) => api.post('/instituciones', data),
  update: (id, data) => api.put(`/instituciones/${id}`, data),
  delete: (id) => api.delete(`/instituciones/${id}`),
};

export const stats = {
  getProgress: () => api.get('/progreso'),
  getMyStats: () => api.get('/estadisticas'),
  getAdminMetrics: () => api.get('/admin/metricas'),
};

export const ai = {
  generarQuiz: (data) => api.post('/ai/generar-quiz', data),
  chat: (data) => api.post('/ai/chat', data),
  resumir: (data) => api.post('/ai/resumir', data),
  status: () => api.get('/ai/status'),
  consultarLectura: (data) => api.post('/ai/consultar-lectura', data),
  explicarPregunta: (data) => api.post('/ai/explicar-pregunta', data),
  misConsultas: () => api.get('/ai/mis-consultas'),
};

export default api;
