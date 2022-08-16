

export const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
    },
    {
        path: '/sign-in',
        name: 'SignIn',
        component: () => import(/* webpackChunkName: "signin" */ '../views/SignIn.vue')
    },
    {
        path: '/last-transactions',
        name: 'LastTransactions',
        component: () => import(/* webpackChunkName: "last-transactions" */ '../views/LastTransactions.vue')
    },
    {
        path: '/save-card',
        name: 'SaveCard',
        component: () => import(/* webpackChunkName: "save-card" */ '../views/SaveCard.vue')
    },
    {
        path: '/save-transaction',
        name: 'SaveTransaction',
        component: () => import(/* webpackChunkName: "save-transaction" */ '../views/SaveTransaction.vue')
    },
    {
        path: '/save-voice-transaction',
        name: 'SaveVoiceTransaction',
        component: () => import(/* webpackChunkName: "save-transaction" */ '../views/SaveVoiceTransaction.vue')
    },
    {
        path: '/search-transaction/:query',
        name: 'SearchTransaction',
        component: () => import(/* webpackChunkName: "search-transaction" */ '../views/SearchTransaction.vue')
    },
    {
        path: '/show-chart',
        name: 'ShowChart',
        component: () => import(/* webpackChunkName: "show-chart" */ '../views/ShowChart.vue')
    },
    {
        path: '/print-account',
        name: 'PrintAccount',
        component: () => import(/* webpackChunkName: "print-account" */ '../views/PrintAccount.vue')
    },
    {
        path: '/chnage-info',
        name: 'ChnageInfo',
        component: () => import(/* webpackChunkName: "chnage-info" */ '../views/ChnageInfo.vue')
    },
    {
        path: '/setting',
        name: 'Setting',
        component: () => import(/* webpackChunkName: "setting" */ '../views/Setting.vue')
    }
]