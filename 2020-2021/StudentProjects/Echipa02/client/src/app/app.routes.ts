import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomeGuestComponent} from './home-guest/home-guest.component';
import {DashboardComponent} from './dashboard/dashboard.component';

const appRoutes: Routes = [
    {path: '', component: HomeGuestComponent},
    {path: 'login', component: HomeGuestComponent},
    {path: 'dashboard', component: DashboardComponent},
];

@NgModule({
    imports: [RouterModule.forRoot(appRoutes)],
    exports: [RouterModule]
})
export class AppRoutes {

}
