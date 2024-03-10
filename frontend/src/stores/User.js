import { createStore } from 'vuex';
import { onMounted } from 'vue';
import axios from 'axios';
import router from "@/router/index.js"

const Userstore =createStore({

    state(){
        return {
            user:{
            username: "",
            email: "",
            role: "",
            token: localStorage.getItem('authtoken') || "",
            },
            error:""
        };
    },

    getters: {
        geterror: (state) => ()=>state.error,
        getuser: (state) => () => state.user,
    },

    mutations:{
        getuser(state,d){
            state.user.username=d.username;
            state.user.email=d.email;
            state.user.role=d.role;
        },
        setuser(state,d){
            state.user.username=d.username;
            state.user.email=d.email;
            state.user.token=d.token;
            state.user.role=d.role;
            localStorage.setItem("authtoken",d.token);
        },
        seterror(state, error) {
            state.error = error;
        },
        clearuser(state) {
            state.user.username = '';
            state.user.email = '';
            state.user.role = '';
            state.user.token = '';
            localStorage.setItem("authtoken")
        },
        clearerror(state) {
            state.error = '';
        }
    },



    actions: {

        clearuser({ commit }) {
            commit('clearuser');
        },
        clearerror({commit}){
            commit('clearerror')
        },

        getuserinfo({ commit }){
            const token=localStorage.getItem('authtoken');
            const path='http://127.0.0.1:5000/api/retreive'
            axios.get(path,{
                headers: {
                    'Authentication-Token': token
                },
            })
            .then((res)=>{
                commit('getuser',res.data);
            })
            .catch((err)=>{
                console.log('no data fetched');
            })

        },

        async authenticate({ commit }){
            const token=localStorage.getItem('authtoken');
            if (!token) {
                return Promise.resolve(false);
              }
     
            const path='http://127.0.0.1:5000/api/authenticate'
            return axios.get(path,{
                headers: {
                    'Authentication-Token': token
                }
            })
            .then((res)=>{
                if (res.data.authenticated){
                    return true;
                }
                else {
                    console.log(res.data.authenticated+"hi");
                    localStorage.removeItem('authtoken');
                    return false;
                }
            })
            .catch(()=>{
                localStorage.removeItem('authtoken');
                return false;
            })
        },

        login({ commit },form){
            const path='http://127.0.0.1:5000/api/login';
            axios.post(path,form,{
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then((res) => {
                commit('setuser',res.data);
                commit('clearerror');
                router.push({name:'home'});
                
            })
            .catch((err)=>{
                commit('seterror', err.response.data.message);
                console.log(this.state.error);
            })
        },

        logout({ commit }){
            localStorage.removeItem('authtoken')
            commit('clearuser');
        },

        register({commit},form){
            const path='http://127.0.0.1:5000/api/register';
            axios.post(path,form,{
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then((res)=>{
                commit('setuser',res.data.userdata)
                commit('clearerror');
                console.log(res.data);
            })
            .catch((err)=>{
                commit('seterror', err.response.data.message);
                console.log(this.state.error);
            })
        }
    }, 

})

export default Userstore;