import {createRouter, createWebHistory} from 'vue-router'
import CouchTable from "@/views/CouchTable.vue";
import BasePageView from "@/views/BasePageView.vue";
import AuthView from "@/views/AuthView.vue";
import ConfirmEmailView from "@/views/ConfirmEmailView.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import ProfileEditor from "@/components/ProfileEditor.vue";
import FormNewClient from "@/views/FormNewClient.vue";
import ClientList from "@/views/ClientList.vue";
import ClientALLList from "@/views/ClientALLList.vue";
import NewClientCouchTable from "@/views/NewClientCouchTable.vue";
import VisitTable from "@/views/VisitTable.vue";

let routes;
routes = [
  {path: '/', component: BasePageView, name: 'base', props: true},
  {path: '/auth', component: AuthView, name: 'auth', props: true},
  {path: '/form', component: FormNewClient, name: 'form', props: true},
  {path: '/confirm_email/:token', component: ConfirmEmailView, name: 'confirmEmail', props: true},
  {path: '/profile', component: ProfilePage, name: 'profile', props: true},
  {path: '/profile/edit', component: ProfileEditor, name: 'profile-editor', props: true},
  {path: '/couch/table', component: CouchTable, name: 'couch-table', props: true},
  {path: '/clients-list/', component: ClientList, name: 'client-list', props: true},
  {path: '/clients-all-list/', component: ClientALLList, name: 'clients-all-list', props: true},
  {path: '/couch/new-client/table', component: NewClientCouchTable, name: 'couch-new-client', props: true},
  {path: '/couch/visit/table', component: VisitTable, name: 'visit-table', props: true},
];

export default createRouter({
  history: createWebHistory(),
  routes,
})
