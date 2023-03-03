import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {

  fileToUpload: any;
  imageUrl: any;
  fileUploaded = false;
  originalAnswer = "Please upload an image to be classified"

  constructor() { }

  ngOnInit(): void {

  }

  handleFileInput(target: any) {

    this.fileToUpload = target.files.item(0);

    //Show image preview
    let reader = new FileReader();
    reader.onload = (event: any) => {
      this.imageUrl = event.target.result;
    }
    reader.readAsDataURL(this.fileToUpload);
    this.fileUploaded = true;
  }

  predictDigit(){
    // TODO: Create prediction method
    console.log('This is prediction!')
  }

}
