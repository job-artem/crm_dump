<template>
    <gb-ui :button-text="'Регистрация через Google'" @click="loginWithGoogle">
    </gb-ui>
</template>

<script>
import {useTokenClient} from "vue3-google-signin";
import axios from "axios";
import GbUi from "@/components/UI/GoogleButtonUI.vue";

export default {
    name: "GoogleRegistration",
  components: {GbUi},
    emits: ["registration-successful", "registration-failed"],
    setup(_, {emit}) {
        const {login} = useTokenClient({
            onSuccess: async ({access_token}) => {
                try {
                    const response = await axios.post("registration/", {token: access_token});
                    emit("registration-successful", response.data);
                } catch (error) {
                    emit("registration-failed", error);
                }
            },
        });

        const loginWithGoogle = async () => {
            await login();
        };

        return {loginWithGoogle};
    },
};
</script>

<style scoped></style>
