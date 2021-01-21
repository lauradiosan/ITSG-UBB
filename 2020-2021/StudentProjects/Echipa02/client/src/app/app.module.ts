import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { AppRoutes } from './app.routes';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material';
import { HomeGuestComponent } from './home-guest/home-guest.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { CookieService } from './services/cookie.service'
import { HttpService } from './services/http.service'

@NgModule({
  declarations: [
    AppComponent,
    HomeGuestComponent,
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutes,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatToolbarModule
  ],
  providers: [
    HttpService,
    CookieService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
