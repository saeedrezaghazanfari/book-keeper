import { createWebHistory } from 'vue-router'
import {routes} from './routes' 
import translations from '../translations'
import { createLangRouter } from 'vue-lang-router'

const langRouterOptions = {
	defaultLanguage: 'fa',
	translations,
}
const routerOptions = {
	history: createWebHistory(),
	routes
}
const router = createLangRouter(langRouterOptions, routerOptions)

export default router
