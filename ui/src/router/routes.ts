import IndexPage from 'pages/IndexPage.vue'
import MainLayout from 'layouts/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [{ path: '', component: IndexPage }]
  }
]

export default routes;
