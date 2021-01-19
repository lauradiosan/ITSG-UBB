import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { HistoryComponent } from './components/history/history.component';
import { LoginRegisterComponent } from './components/login-register/login-register.component';
import { MedicalImageViewerComponent } from './components/medical-image-viewer/medical-image-viewer.component';

const routes: Routes =  [
  { path: "", component: DashboardComponent },
  { path: "medical-image-viewer", component: MedicalImageViewerComponent },
  { path: "login", component: LoginRegisterComponent },
  { path: "history", component: HistoryComponent },
  { path: "**", redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }