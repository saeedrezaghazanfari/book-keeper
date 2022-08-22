<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-image"></i> {{ $t('Backstage Settings') }}</h4>

        <div class="wrapper-bg">
            <div class="bg" @click="$store.commit('CHANGE_BG_CLASS', 'bg-spring')">
                <img :src="require('../assets/img/bg-spring.jpg')" alt="spring image">
                <p>{{ $t('Spring') }}</p>
            </div>
            <div class="bg" @click="$store.commit('CHANGE_BG_CLASS', 'bg-summer')">
                <img :src="require('../assets/img/bg-summer.jpg')" alt="summer image">
                <p>{{ $t('Summer') }}</p>
            </div>
            <div class="bg" @click="$store.commit('CHANGE_BG_CLASS', 'bg-fall')">
                <img :src="require('../assets/img/bg-fall.jpg')" alt="fall image">
                <p>{{ $t('Fall') }}</p>
            </div>
            <div class="bg" @click="$store.commit('CHANGE_BG_CLASS', 'bg-winter')">
                <img :src="require('../assets/img/bg-winter.jpg')" alt="winter image">
                <p>{{ $t('Winter') }}</p>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    name: 'Setting',
    
    async mounted() {
        // check user
        let r_token = JSON.parse(localStorage.getItem('BOOKKEEPER_RT'));
        if(r_token) {
            let formdata = new FormData();
            formdata.append('refresh', r_token)
            await axios.post(`/${this.$i18n.locale}/api/v1/get-token/refresh-token/`, formdata, {
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then((result) => {
                localStorage.setItem('BOOKKEEPER_AT', JSON.stringify(result.data.access));
                this.$store.dispatch('getUserData', {at: result.data.access, lang: this.$i18n.locale});
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            })
        } else {
            this.$router.push('/' + this.$i18n.locale + '/sign-in');
        }
    }
}
</script>

<style scoped>
.opacity-wrapper h4{margin-bottom:1rem}.opacity-wrapper .wrapper-bg{padding:0.5rem;display:flex;flex-wrap:wrap}.opacity-wrapper .wrapper-bg .bg{flex:1;text-align:center;position:relative}.opacity-wrapper .wrapper-bg .bg p{z-index:2;position:absolute;text-align:center;width:100%;opacity:0;bottom:5px;transition:all 0.3s ease;font-size:12pt;text-shadow:3px 3px 3px black}.opacity-wrapper .wrapper-bg .bg img{height:90px;border-radius:50%;width:90px;transition:all 0.3s ease}.opacity-wrapper .wrapper-bg .bg:hover img{filter:blur(3px)}.opacity-wrapper .wrapper-bg .bg:hover p{transform:translateY(-37px);opacity:1}.opacity-wrapper .wrapper-bg .bg:hover p{transform:translateY(-37px);opacity:1}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>