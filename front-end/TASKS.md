await axios.post(`/${this.$i18n.locale}/api/get-token/`,
    formdata, {
        headers: {
            'Authorization': `Token ${exist}`,
            'Content-Type': 'multipart/form-data',
        }
    }
)



<!-- http://www.fromtexttospeech.com/ -->