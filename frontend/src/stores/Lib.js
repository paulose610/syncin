import { createStore } from 'vuex';
import { toRaw } from 'vue';
import axios from 'axios';
import router from "@/router/index.js"
import Userstore from "./User";

const Libstore = createStore({
    state(){
        return {
           playlists: [],
           likedsongs: [],
           albums: [],
           useralbums: [],
           songs: [] ,
           usersongs: [],
        }
    },

    getters:{
            getpl: (state) => () => state.playlists,
            getls: (state) => () => state.likedsongs,
            getalbums: (state) => () => state.albums,
            getuseralbums: (state) => () => state.useralbums,
            getsongs: (state) => () => state.songs,
            getusersongs: (state) => () => state.usersongs,
        },
        

    mutations: {
        setplaylists(state,pl){
            state.playlists=pl;
        },
        
        setlikedsongs(state,ls){
            state.likedsongs=ls;
        },

        setalbums(state,al){
            state.albums=al;
        },

        setuseralbums(state,usal){
            state.useralbums=usal;
        },

        createalbum(state,al){
            state.albums.push(al);
            state.useralbums.push(al);
        },

        editalbum(state,album){
            const index=state.albums.findIndex(s=>s.id==album.id);
            const ualind=state.useralbums.findIndex(s=>s.id==album.id);
            if (index !== -1) {
                const atoedit = state.albums[index];
                state.albums[index] = { ...atoedit, ...album };
            }
            if (ualind !== -1) {
                state.useralbums[ualind]=state.albums[index];
            }

        },

        delalbum(state,delinfo){
            const cond=delinfo.cond;
            const aid=delinfo.id;
            if (cond==1){
                state.usersongs=state.usersongs.filter(s=>s.album_id!=aid);
                state.songs=state.songs.filter(s=>s.album_id!=aid);
            }
            else {
                state.usersongs = state.usersongs.map(s => {
                    if (s.album_id == aid) {
                        return { ...s, album_id: null };
                    }
                    return s;
                });
            
                state.songs = state.songs.map(s => {
                    if (s.album_id == aid) {
                        return { ...s, album_id: null };
                    }
                    return s;
                });    
            }
            state.useralbums=state.useralbums.filter(a=>a.id!=aid);
            state.albums=state.albums.filter(a=>a.id!=aid);
            console.log(state.usersongs);            
        },    

        setsongs(state,s){
            state.songs=s;
        },

        setusersongs(state,us){
            state.usersongs=us
        },

        uploadsong(state,song){
            state.songs.push(song);
            state.usersongs.push(song); 
        },

        editsong(state,song){
            const index=state.songs.findIndex(s=>s.id==song.id);
            const usind=state.usersongs.findIndex(s=>s.id==song.id);
            if (index !== -1) {
                const stoedit = state.songs[index];
                state.songs[index] = { ...stoedit, ...song };
            }
            if (usind!==-1){
                state.usersongs[usind]=state.songs[index];
            }
        },

        delsong(state,id){
            const ind=state.songs.findIndex(s=>s.id==id);
            const usind=state.usersongs.findIndex(s=>s.id==id);
            state.songs.splice(ind,1);
            state.usersongs.splice(usind,1);
        },
    },    

    actions: {

        async loadpl({ commit },user){
            const path='http://127.0.0.1:5000/api/playlists';
            const token=localStorage.getItem('authtoken');
            return axios.get(path,{
                headers:{
                    'Authentication-Token': token
                }    
            })
            .then((res)=>{
                commit('setplaylists',res.data);
            })
            .catch((err)=>{
                console.log("couldn't load playlists!");
            })
        },

        async loadls({ commit }){
            const path='http://127.0.0.1:5000/api/likedsongs';
            const token=localStorage.getItem('authtoken');
            return axios.get(path,{
                headers:{
                    'Authentication-Token': token
                } 
            })
            .then((res)=>{
                commit('setlikedsongs',res.data);
            })
            .catch((err)=>{
                console.log("couldn't load liked songs!");
            })
        },

        async loadalbums({ commit }, user){
            const path='http://127.0.0.1:5000/api/albums';
            return axios.get(path,{
                params: {
                    uid: user.id,
                    ur: user.role 
                }
            })
            .then((res)=>{
                commit('setalbums',res.data['allalbums']);
                if (user.role==='creator'){
                    commit ('setuseralbums', res.data['albums']);
                }
            })
            .catch((err)=>{
                console.log("couldn't load albums");
            })
        },

        createalbum({ commit },album){
            console.log(album)
            commit('createalbum', album);
        },

        editalbum({ commit },album){
            console.log(album);
            commit('editalbum',album);
        },

        delalbum({ commit },delinfo){
            commit('delalbum',delinfo);
        },

        async loadsongs({ commit }, user){
            const path='http://127.0.0.1:5000/api/songs'
            return axios.get(path,{
                params: {
                    uid: user.id,
                    ur: user.role 
                }
            })
            .then((res)=>{
                commit('setsongs',res.data['allsongs']);
                if (user.role==='creator'){
                    commit ('setusersongs', res.data['songs']);
                }
            })
        },

        uploadsong({ commit },song){
            console.log(song);
            commit('uploadsong',song);
        },

        editsong({commit},song){
            console.log(song);
            commit('editsong',song);
        },

        delsong({ commit }, sid){
            console.log(sid);
            commit('delsong',sid);
        },

        async libload({ dispatch },user){
            await dispatch('loadls',user);
            await dispatch('loadpl',user);
            await dispatch('loadalbums',user);
            await dispatch('loadsongs',user);
        },

    },
})

export default Libstore;