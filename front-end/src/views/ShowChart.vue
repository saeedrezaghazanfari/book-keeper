<template>
    <div class="opacity-wrapper" ref="ow_fullpage" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-stats-up"></i> {{ $t('Show Charts') }}</h4>

        <div class="wrapper-gotoallpage" v-if="show_gotoallpage">
            <p>{{ $t('If you want to see the Chart in Full Screen, Click on the Button below') }}</p>
            <div class="wrapper_btns">
                <button @click="go_to_full_page"><i class="ti-fullscreen"></i></button>
                <button @click="go_to_continue"><i class="ti-back-left"></i></button>
            </div>
        </div>

        <form @submit.prevent="get_charts_data" novalidate>
            <ul class="wrapper-lines">
                <li @click="go_to_full_page" v-if="show_fs_mode" class="mb-1">
                    <i class="text-light link ti-fullscreen"></i> <span class="text-light link">{{ $t('Go to Full Screen') }}</span>
                </li>
                <li @click="reset_div" v-else class="mb-1">
                    <i class="text-light link" :class="{'ti-arrow-left': $i18n.locale == 'fa', 'ti-arrow-right': $i18n.locale == 'en'}"></i> <span class="text-light link">{{ $t('Go Back') }}</span>
                </li>
            </ul>
            <div class="three-forminput-control">
                <select v-if="!show_reload_icon" type="text" required v-model="all_or_bankname">
                    <option value="all">{{ $t('All of Banks') }}</option>
                    <option v-for="(bank, index) in banks" :key="index" :value="bank.name">{{ bank.name }}</option>
                </select>
                <select v-if="!show_reload_icon" type="text" required v-model="period">
                    <option value="select">{{ $t('Select a Time Interval') }}</option>
                    <option value="7">{{ $t('Weekly') }}</option>
                    <option value="30">{{ $t('Monthly') }}</option>
                    <option value="90">{{ $t('Trimester') }}</option>
                    <option value="180">{{ $t('Six months') }}</option>
                    <option value="365">{{ $t('One year') }}</option>
                </select>
                <select v-if="!show_reload_icon" type="text" required v-model="type_transactions">
                    <option value="withdrawal">{{ $t('Withdrawals') }}</option>
                    <option value="deposit">{{ $t('Deposits') }}</option>
                </select>
                <select v-if="!show_reload_icon" type="text" required v-model="type_chart">
                    <option value="line">{{ $t('Line') }}</option>
                    <option value="bar">{{ $t('Bar') }}</option>
                    <option value="doughnut">{{ $t('Doughnut') }}</option>
                </select>

                <button class="d-none data_btnc" ref="data_btncc"><span class="mx-1-2">{{all_or_bankname == 'all' ? $t('All Banks') : all_or_bankname}}</span> <span class="mx-1-2">{{period + $t('Days')}}</span> <span class="mx-1-2">{{$t(type_transactions)}}</span></button><br>
                <button class="d-none btn-chart" ref="line_btnc" @click="show_line_chart">{{ $t('Line Chart') }} <i class="ti-line-double"></i></button>
                <button class="d-none btn-chart" ref="bar_btnc" @click="show_bar_chart">{{ $t('Bar Chart') }} <i class="ti-bar-chart"></i></button>
                <button class="d-none btn-chart" ref="doughnut_btnc" @click="show_doughnut_chart">{{ $t('Doughnut Chart') }} <i class="ti-pie-chart"></i></button>
                <button @click="$router.go()" class="btn reload-btn d-none" ref="reload_btn_ref">{{ $t('Reload') }}</button>

                <button v-if="!show_reload_icon" type="submit" ref="submit_btn_ref" :disabled="!!(period == 'select') == true" :class="period == 'select' ? 'disabled btn' : 'btn'">{{ $t('Show Charts') }}</button>
            </div>
        </form>
        <br>

        <div ref="bar_chart_div" class="d-none">
            <vue3-chart-js
                :id="chart1.id"
                :type="chart1.type"
                :data="chart1.data"
                @before-render="beforeRenderLogic"
            ></vue3-chart-js>
        </div>

        <div ref="line_chart_div" class="d-none">
            <vue3-chart-js
                :id="chart2.id"
                :type="chart2.type"
                :data="chart2.data"
                @before-render="beforeRenderLogic"
            ></vue3-chart-js>
        </div>

        <div ref="doughnut_chart_div" class="d-none">
            <vue3-chart-js
                :id="chart3.id"
                :type="chart3.type"
                :data="chart3.data"
                @before-render="beforeRenderLogic"
            ></vue3-chart-js>
        </div>

    </div>
</template>

<script>
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs';
import axios from '../plugins/axios';

export default {
    name: 'ShowChart',

    components: { Vue3ChartJs },

    data: () => ({
        chart1: {
            id: 'chart-1',
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: '#',
                    data: [],
                    backgroundColor: [],
                    borderColor: [],
                    fill: true,
                    borderWidth: 1
                }]
            }
        },

        chart2: {
            id: 'chart-2',
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: '#',
                    data: [],
                    backgroundColor: [],
                    borderColor: [],
                    fill: true,
                    borderWidth: 1
                }]
            }
        },

        chart3: {
            id: 'chart-3',
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    label: '#',
                    data: [],
                    backgroundColor: [],
                    borderColor: [],
                    fill: true,
                    borderWidth: 1
                }]
            }
        },

        show_gotoallpage: true,
        banks: '',
        all_or_bankname: 'all',
        period: 'select',
        type_transactions: 'withdrawal',
        type_chart: 'bar',
        show_fs_mode: true,
        show_reload_icon: false
    }),

    created() { 
        this.get_banks();
        this.chart1.data.datasets[0].backgroundColor = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'];
        this.chart1.data.datasets[0].borderColor = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'];
        this.chart2.data.datasets[0].backgroundColor = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'];
        this.chart2.data.datasets[0].borderColor = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'];
        this.chart3.data.datasets[0].backgroundColor = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'];
        this.chart3.data.datasets[0].borderColor = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'];
    },

    methods: {

        go_to_full_page() {
            this.$refs.ow_fullpage.classList.add('opacity-wrapper-fullpage');
            this.show_fs_mode = false;
            this.show_gotoallpage = false;
        },

        go_to_continue() {
            this.show_gotoallpage = false;
        },

        reset_div() {
            this.$refs.ow_fullpage.classList.remove('opacity-wrapper-fullpage');
            this.show_fs_mode = true;
        },
        
        async get_charts_data() {
            // this.chart3.data.datasets[0].data = [1,2,3]
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            let formdata = new FormData();
            formdata.append('all_or_bankname', this.all_or_bankname);
            formdata.append('period', this.period);
            formdata.append('type_transactions', this.type_transactions);
            await axios.post(`/${this.$i18n.locale}/api/v1/get-chart/`, formdata, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.data.status === 200) {
                    this.$refs.submit_btn_ref.classList.add('d-none');
                    this.$refs.reload_btn_ref.classList.remove('d-none');
                    this.$refs.data_btncc.classList.remove('d-none');
                    this.$refs.line_btnc.classList.remove('d-none');
                    this.$refs.bar_btnc.classList.remove('d-none');
                    this.$refs.doughnut_btnc.classList.remove('d-none');
                    this.$refs.line_chart_div.classList.add('d-none');
                    this.$refs.bar_chart_div.classList.add('d-none');
                    this.$refs.doughnut_chart_div.classList.add('d-none');
                    this.show_reload_icon = true;
                    if(this.type_chart == 'line') this.$refs.line_chart_div.classList.remove('d-none');
                    else if(this.type_chart == 'bar') this.$refs.bar_chart_div.classList.remove('d-none');
                    else if(this.type_chart == 'doughnut') this.$refs.doughnut_chart_div.classList.remove('d-none');

                    this.chart1.data.labels = [];
                    this.chart2.data.labels = [];
                    this.chart3.data.labels = [];
                    this.chart1.data.datasets[0].data = [];
                    this.chart2.data.datasets[0].data = [];
                    this.chart3.data.datasets[0].data = [];

                    result.data.items.map((obj)=> {
                        this.chart1.data.labels.push(obj);
                    });
                    result.data.items.map((obj)=> {
                        this.chart2.data.labels.push(obj);
                    });
                    result.data.items.map((obj)=> {
                        this.chart3.data.labels.push(obj);
                    });

                    result.data.prices.map((obj)=> {
                        this.chart1.data.datasets[0].data.push(obj);
                    });
                    result.data.prices.map((obj)=> {
                        this.chart2.data.datasets[0].data.push(obj);
                    });
                    result.data.prices.map((obj)=> {
                        this.chart3.data.datasets[0].data.push(obj);
                    });
                }
            })
            .catch((err) => {
                if(err.response.status === 401) {
                    this.$router.push('/' + this.$i18n.locale + '/sign-in');
                }
            });
        },

        show_line_chart() {
            this.type_chart = 'line';

            this.$refs.line_chart_div.classList.remove('d-none');
            this.$refs.line_btnc.classList.add('d-none');

            this.$refs.bar_chart_div.classList.add('d-none');
            this.$refs.bar_btnc.classList.remove('d-none');

            this.$refs.doughnut_chart_div.classList.add('d-none');
            this.$refs.doughnut_btnc.classList.remove('d-none');

        },
        show_bar_chart() {
            this.type_chart = 'bar';
            this.$refs.bar_chart_div.classList.remove('d-none');
            this.$refs.bar_btnc.classList.add('d-none');

            this.$refs.line_chart_div.classList.add('d-none');
            this.$refs.line_btnc.classList.remove('d-none');

            this.$refs.doughnut_chart_div.classList.add('d-none');
            this.$refs.doughnut_btnc.classList.remove('d-none');
        },
        show_doughnut_chart() {
            this.type_chart = 'doughnut';
            this.$refs.doughnut_chart_div.classList.remove('d-none');
            this.$refs.doughnut_btnc.classList.add('d-none');

            this.$refs.bar_chart_div.classList.add('d-none');
            this.$refs.bar_btnc.classList.remove('d-none');

            this.$refs.line_chart_div.classList.add('d-none');
            this.$refs.line_btnc.classList.remove('d-none');
        },

        async get_banks() {
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            await axios.get(`/${this.$i18n.locale}/api/v1/card-management/`, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.status === 200) {
                    this.banks = result.data.data;
                }
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            });
        },

        beforeRenderLogic(event){
        },
    },

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
.opacity-wrapper{
    width: 82% !important;
    min-height: 83% !important;
    background-color: #000000f5 !important;
}
.btn-chart, .data_btnc {
    padding: 8px 13px;
    border-radius: 5px;
    background: linear-gradient(rgb(77, 77, 77), rgb(31, 31, 31));
    cursor: url(../assets/img/cursor-link.png),auto;
    position: relative;
    transition: all 0.3s ease;
    color: white;
    border-bottom: 1px solid rgb(214, 214, 214);
}
.data_btnc {
    background: linear-gradient(rgb(77, 77, 77), rgb(31, 31, 31));
    cursor: none;
    color: rgb(201, 201, 201);
    border-bottom: none;
}
.data_btnc span {cursor: none;}
ul {list-style: none;}
.opacity-wrapper ul.wrapper-lines li{padding:0px 18px; color:white;transition:all 0.3s ease;font-size:12pt}
.opacity-wrapper ul.wrapper-lines li i{font-size: 10pt;}
.opacity-wrapper-fullpage {
    position: fixed !important;
}
.wrapper_btns {
    display: flex;
    margin-top: 10px;
}
.wrapper_btns button {
    margin: 0 10px;
}
.wrapper-gotoallpage {
    position: absolute;
    inset: 0;
    background-color: rgba(0,0,0,0.87);
    z-index: 100;
    padding: 2rem;
    text-align: center;
    display: flex;
    align-items: center;
    border-radius: 15px;
    justify-content: center;
    flex-direction: column;
    transition: all 0.3s ease;
}
.wrapper-gotoallpage p {
    padding-bottom: 20px;
}
.wrapper-gotoallpage button {
    padding: 14px 15px;
    border-radius: 50%;
    background: linear-gradient(rgb(77, 77, 77), rgb(31, 31, 31));
    cursor: url(../assets/img/cursor-link.png),auto;
    position: relative;
    transition: all 0.3s ease;
}
.wrapper-gotoallpage button:hover {
    transform: scale(1.02);
}
.wrapper-gotoallpage button::before {
    content: '';
    position: absolute;
    border-radius: 50%;
    inset: 0;
    background-color: rgba(255, 255, 255, 0.1);
    animation: faderBtn 1.5s infinite linear;
}
@keyframes faderBtn {
    0% {
        transform: scale(1);
        opacity: 1;
    }
    75% {
        transform: scale(1.4);
        opacity: 0.2;
    }
    100% {
        transform: scale(1.4);
        opacity: 0;
    }
}
.wrapper-gotoallpage button i {font-size: 30pt;cursor: url(../assets/img/cursor-link.png),auto;color: white;}
.reload-btn{color: white;background-color: #7d00006e;padding: 8px 13px;border-radius: 5px;}.opacity-wrapper h4{margin-bottom:1rem}.opacity-wrapper .three-forminput-control{display:flex;flex-wrap:wrap;position:relative}.opacity-wrapper .three-forminput-control select{min-width:150px;padding:6px 0;font-size:11pt;color:#fff;margin:0 5px 5px 5px;border:none;border-bottom:1px solid #fff;background:#2424244f;width:100% !important}.opacity-wrapper .three-forminput-control button[type="submit"]{color:white;background-color:#0000006e;padding:0.3rem 1rem;border-radius:5px;min-width:150px}.opacity-wrapper .three-forminput-control select{flex:2}.opacity-wrapper .three-forminput-control button[type="submit"]{flex:1}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{overflow-x:auto}}
</style>