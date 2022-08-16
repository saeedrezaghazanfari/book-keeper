import axios from '../plugins/axios';

export default {

    async getUserData(context, payload) {
        await axios.get(`/${payload.lang}/api/v1/get-user-data/`, {
            headers: {
                'Authorization': `Bearer ${payload.at}`,
            }
        })
        .then((result) => {
            if(result.data.status === 200) {
                context.commit('SAVE_USER_DATA', result.data.data);
            }
        })
    }
}