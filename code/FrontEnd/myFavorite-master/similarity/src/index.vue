
<script>
    import main from './main';
    export default {
        data: function(){
            return {
                dialogVisible:false,
                data:[]
            }
        },
        created(){
            this.init();
        },
        methods: {
            init(){
                this.$http.post(main.url+"/favorite/list",
                    {'uid': 0},
                    {
                        headers: {'Content-Type':'application/x-www-form-urlencoded'},
                        emulateJSON: true
                    }).then(
                    success=>{
                        this.data=success.data;
                    }
                );
            },
            gotourl(row){ //进入指定的网站
                this.$http.post(main.url+"/favorite/count",
                    {'id': row.id},
                    {
                        headers: {'Content-Type':'application/x-www-form-urlencoded'},
                        emulateJSON: true
                    }).then(
                    success=> {
                        window.open(row.wurl, "_blank");
                        this.init();
                    }
                )
            },
            submit(){
                this.$router.push({ path: '/login' });
            }
        }
    }
</script>

<style scoped>
    .tab{
        position: absolute;
        top: 20%;
        left: 25%;
        width: 805px;
        height: 100%;
    }
    .login-wrap{
        position: relative;
        background: url("/static/img/bg.jpg") no-repeat center;
        width:100%;
        height:100%;
    }
    .ms-title{
        position: absolute;
        top: 40%;
        width: 100%;
        margin-top: -230px;
        text-align: center;
        font-size: 14px;
        color: #fff;
        font-weight: bold;
    }
    .login-btn button{
        position: absolute;
        width: 40%;
        height: 35px;
        right: 10%;
        top: 10%;
    }
</style>
