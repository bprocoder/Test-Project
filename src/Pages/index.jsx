import React from './react';

class index extends React.Component(){
    render(){
        return
        ()

        };
    };
}

<div id="wrapper">
  <div className="topbar">
    <div className="topbar-left">
      <a href="index.html" className="logo"><img src="assets/images/logo.png" alt style={{width: 'auto', height: 67}} /></a>
    </div>
    <nav className="navbar-custom">
      <ul className="navbar-right d-flex list-inline float-right mb-0">
        <li className="dropdown notification-list d-none d-sm-block">
          <form role="search" className="app-search">
            <div className="form-group mb-0"> 
              <input type="text" className="form-control" placeholder="Search.." />
              <button type="submit"><i className="fa fa-search" /></button>
            </div>
          </form> 
        </li>
        <li className="dropdown notification-list">
          <a className="nav-link dropdown-toggle arrow-none waves-effect" data-toggle="dropdown" href="#" role="button" aria-haspopup="false" aria-expanded="false">
            <i className="ti-bell noti-icon" />
            <span className="badge badge-pill badge-danger noti-icon-badge">3</span>
          </a>
          <div className="dropdown-menu dropdown-menu-right dropdown-menu-lg">
            {/* item*/}
            <h6 className="dropdown-item-text">
              Notifications (258)
            </h6>
            <div className="slimscroll notification-item-list">
              {/* item*/}
              <a href="javascript:void(0);" className="dropdown-item notify-item active">
                <div className="notify-icon bg-success"><i className="mdi mdi-cart-outline" /></div>
                <p className="notify-details">Your order is placed<span className="text-muted">Dummy text of the printing and typesetting industry.</span></p>
              </a>
              {/* item*/}
              <a href="javascript:void(0);" className="dropdown-item notify-item">
                <div className="notify-icon bg-warning"><i className="mdi mdi-message" /></div>
                <p className="notify-details">New Message received<span className="text-muted">You have 87 unread messages</span></p>
              </a>
              {/* item*/}
              <a href="javascript:void(0);" className="dropdown-item notify-item">
                <div className="notify-icon bg-info"><i className="mdi mdi-martini" /></div>
                <p className="notify-details">Your item is shipped<span className="text-muted">It is a long established fact that a reader will</span></p>
              </a>
              {/* item*/}
              <a href="javascript:void(0);" className="dropdown-item notify-item">
                <div className="notify-icon bg-primary"><i className="mdi mdi-cart-outline" /></div>
                <p className="notify-details">Your order is placed<span className="text-muted">Dummy text of the printing and typesetting industry.</span></p>
              </a>
              {/* item*/}
              <a href="javascript:void(0);" className="dropdown-item notify-item">
                <div className="notify-icon bg-danger"><i className="mdi mdi-message" /></div>
                <p className="notify-details">New Message received<span className="text-muted">You have 87 unread messages</span></p>
              </a>
            </div>
            {/* All*/}
            <a href="javascript:void(0);" className="dropdown-item text-center text-primary">
              View all <i className="fi-arrow-right" />
            </a>
          </div>        
        </li>
        <li className="dropdown notification-list">
          <div className="dropdown notification-list nav-pro-img">
            <a className="dropdown-toggle nav-link arrow-none waves-effect nav-user" data-toggle="dropdown" href="#" role="button" aria-haspopup="false" aria-expanded="false">
              <img src="assets/images/users/user-4.jpg" alt="user" className="rounded-circle" />
            </a>
            <div className="dropdown-menu dropdown-menu-right profile-dropdown ">
              {/* item*/}
              <a className="dropdown-item" href="profile.html"><i className="mdi mdi-account-circle m-r-5" /> Profile</a> 
              <a className="dropdown-item d-block" href="#"><i className="mdi mdi-settings m-r-5" /> Settings</a> 
              <a className="dropdown-item" href="document-wallet.html"><i className="mdi mdi-wallet m-r-5" /> Document Wallet</a>
              <div className="dropdown-divider" />
              <a className="dropdown-item text-danger" href="#"><i className="mdi mdi-power text-danger" /> Logout</a>
            </div>                                                                    
          </div>
        </li>
      </ul>
      <ul className="list-inline menu-left mb-0">
        <li className="float-left">
          <button className="button-menu-mobile open-left waves-effect">
            <i className="mdi mdi-menu" />
          </button>
        </li>
      </ul>
    </nav>
  </div>
  {/* Top Bar End */}
  {/* ========== Left Sidebar Start ========== */}
  <div className="left side-menu">
    <div className="slimscroll-menu" id="remove-scroll">
      {/*- Sidemenu */}
      <div id="sidebar-menu">
        {/* Left Menu Start */}
        <ul className="metismenu" id="side-menu">
          <li>
            <a href="index.html" className="waves-effect">
              <i className="mdi mdi-view-dashboard" /><span className="badge badge-primary badge-pill float-right">2</span> <span> Dashboard </span>
            </a>
          </li>
          <li><a href="javascript:void(0);" className="waves-effect"><i className="mdi mdi-buffer" /><span>
                Start a Business<span className="float-right menu-arrow"><i className="mdi mdi-chevron-right" /></span> </span></a>
            <ul className="submenu">                                   
              <li><a href="popular-options.html">Popular Options</a></li>
              <li><a href="special-business-entities.html">Special Business Entities</a></li> 
            </ul>
          </li>
          <li><a href="javascript:void(0);" className="waves-effect"><i className="mdi mdi-clipboard-outline" /><span>
                Intellectual Property<span className="float-right menu-arrow"><i className="mdi mdi-chevron-right" /></span> </span></a>
            <ul className="submenu">                                   
              <li><a href="trademark.html">Trademark</a></li>
              <li><a href="patent.html">Patent</a></li> 
              <li><a href="copyright.html">Copyright</a></li>
            </ul>
          </li>
          <li><a href="javascript:void(0);" className="waves-effect"><i className="mdi mdi-google-pages" /><span>
                Changes in Business<span className="float-right menu-arrow"><i className="mdi mdi-chevron-right" /></span> </span></a>
            <ul className="submenu">                                   
              <li><a href="select-conversion-type.html">Select Conversion Type</a></li>
              <li><a href="update-corporate-information.html">Update Corporate Information</a></li> 
              <li><a href="close-a-business.html">Close a Business</a></li>
            </ul>
          </li>                     
          <li><a href="javascript:void(0);" className="waves-effect"><i className="mdi mdi-account-location" /><span>
                Registration and Licenses<span className="float-right menu-arrow"><i className="mdi mdi-chevron-right" /></span> </span></a>
            <ul className="submenu">                                   
              <li><a href="government-registration.html">Government Registration</a></li>
              <li><a href="licenses.html">Licenses</a></li>  
            </ul>
          </li>                         
          <li><a href="javascript:void(0);" className="waves-effect"><i className="mdi mdi-account-location" /><span>
                Compliances<span className="float-right menu-arrow"><i className="mdi mdi-chevron-right" /></span> </span></a>
            <ul className="submenu">                                   
              <li><a href="under-compliances.html">Under Compliances</a></li> 
            </ul>
          </li>                      
          <li><a href="javascript:void(0);" className="waves-effect"><i className="mdi mdi-account-location" /><span>
                Tax Return Filings<span className="float-right menu-arrow"><i className="mdi mdi-chevron-right" /></span> </span></a>
            <ul className="submenu">                                   
              <li><a href="tax-return-filings.html">Tax Return Filings</a></li> 
            </ul>
          </li>  
          <li><a href="javascript:void(0);" className="waves-effect"><i className="mdi mdi-account-location" /><span>
                Contact Us<span className="float-right menu-arrow"><i className="mdi mdi-chevron-right" /></span> </span></a>
            <ul className="submenu">                                   
              <li><a href="contact-us.html">Contact us</a></li> 
            </ul>
          </li>                     
        </ul>
      </div>
      {/* Sidebar */}
      <div className="clearfix" />
    </div> 
  </div>
  <div className="content-page">
    {/* Start content */}
    <div className="content">
      <div className="container-fluid">
        <div className="row">
          <div className="col-sm-12">
            <div className="page-title-box">
              <h4 className="page-title">Dashboard</h4>
              <ol className="breadcrumb">
                <li className="breadcrumb-item active">
                  Welcome to NG-Associates Dashboard
                </li>
              </ol>
            </div>
          </div>
        </div>
        {/* end row */}
        <div className="row">
          <div className="col-lg-12">
            <div className="card m-b-20"> 
              {/* Nav tabs */}
              <ul className="nav nav-tabs" role="tablist">
                <li className="nav-item">
                  <a className="nav-link active" data-toggle="tab" href="#account-overview" role="tab">
                    <span className="d-block d-sm-none"><i className="fas fa-home" /></span>
                    <span className="d-none d-sm-block">Account Overview</span> 
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#orders" role="tab">
                    <span className="d-block d-sm-none"><i className="far fa-user" /></span>
                    <span className="d-none d-sm-block">Orders</span> 
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#documents" role="tab">
                    <span className="d-block d-sm-none"><i className="fas fa-cog" /></span>
                    <span className="d-none d-sm-block">Documents</span>    
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#legal-forms" role="tab">
                    <span className="d-block d-sm-none"><i className="fas fa-cog" /></span>
                    <span className="d-none d-sm-block">Legal Forms</span>    
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#profile" role="tab">
                    <span className="d-block d-sm-none"><i className="fas fa-cog" /></span>
                    <span className="d-none d-sm-block">Profile</span>    
                  </a>
                </li>  
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#feedback" role="tab">
                    <span className="d-block d-sm-none"><i className="fas fa-cog" /></span>
                    <span className="d-none d-sm-block">Feedback</span>    
                  </a>
                </li>  
              </ul>
              {/* Tab panes */}
              <div className="tab-content">
                <div className="tab-pane active" id="account-overview" role="tabpanel">
                  <div id="accordion">
                    <div className="mb-2">
                      <div className="card-header p-3" id="headingOne">
                        <h6 className="m-0 font-14">
                          <a href="#collapseOne" className="text-dark" data-toggle="collapse" aria-expanded="true" aria-controls="collapseOne">
                            <div className="account_overview">
                              <div className="left">
                                <i className="far fa-address-book" />
                                <div className="icon">2</div>
                              </div>
                              <div className="right">
                                <h3>Open Order</h3>
                                <p>You have no open orders.</p>
                              </div>
                              <div className="view btn btn-primary">View </div>
                            </div>
                          </a>
                        </h6>
                      </div>
                      <div id="collapseOne" className="collapse " aria-labelledby="headingOne" data-parent="#accordion">
                        <div className="card-body">
                          Anim pariatur cliche reprehenderit,
                        </div>
                      </div>
                    </div>
                    <div className="mb-2">
                      <div className="card-header p-3" id="headingTwo">
                        <h6 className="m-0 font-14">
                          <a href="#collapseTwo" className="text-dark collapsed" data-toggle="collapse" aria-expanded="false" aria-controls="collapseTwo">
                            <div className="account_overview">
                              <div className="left">
                                <i className="dripicons-document" />
                                <div className="icon">2</div>
                              </div>
                              <div className="right">
                                <h3>Queries in Uploaded Document.</h3>
                                <p>There are no Queries in uploaded document.</p>
                              </div>
                              <div className="view btn btn-primary">View</div>
                            </div>
                          </a>
                        </h6>
                      </div>
                      <div id="collapseTwo" className="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
                        <div className="card-body">
                          Anim pariatur cliche reprehenderit, enim eiusmod high life
                          accusamus terry richardson ad squid. 3 wolf moon officia
                          aute, non cupidatat skateboard dolor brunch. Food truck
                          quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor,
                          sunt aliqua put a bird on it squid single-origin coffee
                          nulla assumenda shoreditch et. Nihil anim keffiyeh
                          helvetica, craft beer labore wes anderson cred nesciunt
                          sapiente ea proident. Ad vegan excepteur butcher vice lomo.
                          Leggings occaecat craft beer farm-to-table, raw denim
                          aesthetic synth nesciunt you probably haven't heard of them
                          accusamus labore sustainable VHS.
                        </div>
                      </div>
                    </div>
                    <div className="mb-2">
                      <div className="card-header p-3" id="headingThree">
                        <h6 className="m-0 font-14">
                          <a href="#collapseThree" className="text-dark collapsed" data-toggle="collapse" aria-expanded="false" aria-controls="collapseThree">
                            <div className="account_overview">
                              <div className="left">
                                <i className="far fa-folder-open " />
                                <div className="icon">2</div>
                              </div>
                              <div className="right">
                                <h3>Pending Documents</h3>
                                <p>There are no Documents pending in your Order.</p>
                              </div>
                              <div className="view btn btn-primary">View</div>
                            </div>
                          </a>
                        </h6>
                      </div>
                      <div id="collapseThree" className="collapse" aria-labelledby="headingThree" data-parent="#accordion">
                        <div className="card-body">
                          Anim pariatur cliche reprehenderit, enim eiusmod high life
                          accusamus terry richardson ad squid. 3 wolf moon officia
                          aute, non cupidatat skateboard dolor brunch. Food truck
                          quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor,
                          sunt aliqua put a bird on it squid single-origin coffee
                          nulla assumenda shoreditch et. Nihil anim keffiyeh
                          helvetica, craft beer labore wes anderson cred nesciunt
                          sapiente ea proident. Ad vegan excepteur butcher vice lomo.
                          Leggings occaecat craft beer farm-to-table, raw denim
                          aesthetic synth nesciunt you probably haven't heard of them
                          accusamus labore sustainable VHS.
                        </div>
                      </div>
                    </div>                                            
                    <div className="mb-2">
                      <div className="card-header p-3" id="headingFour">
                        <h6 className="m-0 font-14">
                          <a href="#collapseFour" className="text-dark collapsed" data-toggle="collapse" aria-expanded="false" aria-controls="collapseFour">
                            <div className="account_overview">
                              <div className="left">
                                <i className="dripicons-trophy" />
                                <div className="icon">2</div>
                              </div>
                              <div className="right">
                                <h3>Plan Expire!</h3>
                                <p>There are no plans expire.</p>
                              </div>
                              <div className="view btn btn-primary">View</div>
                            </div>
                          </a>
                        </h6>
                      </div>
                      <div id="collapseFour" className="collapse" aria-labelledby="headingFour" data-parent="#accordion">
                        <div className="card-body">
                          Anim pariatur cliche reprehenderit, enim eiusmod high life
                          accusamus terry richardson ad squid. 3 wolf moon officia
                          aute, non cupidatat skateboard dolor brunch. Food truck
                          quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor,
                          sunt aliqua put a bird on it squid single-origin coffee
                          nulla assumenda shoreditch et. Nihil anim keffiyeh
                          helvetica, craft beer labore wes anderson cred nesciunt
                          sapiente ea proident. Ad vegan excepteur butcher vice lomo.
                          Leggings occaecat craft beer farm-to-table, raw denim
                          aesthetic synth nesciunt you probably haven't heard of them
                          accusamus labore sustainable VHS.
                        </div>
                      </div>
                    </div>
                    <div className="mb-2">
                      <div className="card-header p-3" id="headingFive">
                        <h6 className="m-0 font-14">
                          <a href="#collapseFive" className="text-dark collapsed" data-toggle="collapse" aria-expanded="false" aria-controls="collapseFive">
                            <div className="account_overview">
                              <div className="left">
                                <i className="far fa-address-book" />
                                <div className="icon">2</div>
                              </div>
                              <div className="right">
                                <h3>Documents</h3>
                                <p>There are no uploaded documents.</p>
                              </div>
                              <div className="view btn btn-primary">View</div>
                            </div>
                          </a>
                        </h6>
                      </div>
                      <div id="collapseFive" className="collapse" aria-labelledby="headingFive" data-parent="#accordion">
                        <div className="card-body">
                          Anim pariatur cliche reprehenderit, enim eiusmod high life
                          accusamus terry richardson ad squid. 3 wolf moon officia
                          aute, non cupidatat skateboard dolor brunch. Food truck
                          quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor,
                          sunt aliqua put a bird on it squid single-origin coffee
                          nulla assumenda shoreditch et. Nihil anim keffiyeh
                          helvetica, craft beer labore wes anderson cred nesciunt
                          sapiente ea proident. Ad vegan excepteur butcher vice lomo.
                          Leggings occaecat craft beer farm-to-table, raw denim
                          aesthetic synth nesciunt you probably haven't heard of them
                          accusamus labore sustainable VHS.
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="tab-pane p-3" id="orders" role="tabpanel">
                  <div className="table-responsive">
                    <table className="table table-bordered">
                      <thead>
                        <tr>
                          <th>Service Name</th>
                          <th>Date</th>
                          <th>Payment</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>Private Limited Company Registration</td>
                          <td>15/03/2022</td>
                          <td><a href="#" className="btn btn-success">success</a></td>
                          <td><a href="#" className="btn btn-warning">Pending</a></td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div className="tab-pane p-3" id="documents" role="tabpanel">
                  <div className="form-group">
                    <div className="row">
                      <div className="col-lg-2"><label htmlFor="fullName">Document Name</label></div>
                      <div className="col-lg-4"><input type="text" className="form-control" id placeholder="Type Document Name" /></div>
                      <div className="col-lg-4"> <input type="file" className="form-control" /></div>
                    </div>
                  </div>
                  <div className="form-group">
                    <div className="row">
                      <a href className="btn btn-primary"><i className="fa fa-folder-open" /> Upload</a>
                    </div></div>                                   	
                  <div className="row">                                          	                       	                                         	                       	
                    <div className="col-lg-4"><img src="assets/images/aadharcard.jpg" width="100%" height="auto" alt /></div>       
                    <div className="col-lg-4"><img src="assets/images/pancard.jpg" width="100%" height="auto" alt /></div>  
                    <div className="col-lg-4"><img src="assets/images/gst_cert.jpg" width="100%" height="auto" alt /></div>    
                  </div>                               	                      	
                </div>
                <div className="tab-pane p-3" id="legal-forms" role="tabpanel">
                  <div className="row">
                    <div className="document_name">
                      <ul>
                        <li>Private Limited Company Registration Form <a href className="btn btn-primary">Download Form</a></li>
                        <li>Limited Liability Partnership Registration Form  <a href className="btn btn-primary">Download Form</a></li>
                        <li>One Person Company Registration Form  <a href className="btn btn-primary">Download Form</a></li>
                        <li>Partnership Firm Registration Form  <a href className="btn btn-primary">Download Form</a></li>
                        <li>Sale Proprietarship Form  <a href className="btn btn-primary">Download Form</a></li>
                      </ul>
                    </div>
                  </div>
                </div>
                <div className="tab-pane p-3" id="profile" role="tabpanel">
                  <div className="container">
                    <div className="row gutters">
                      <div className="col-xl-3 col-lg-3 col-md-12 col-sm-12 col-12"> 
                        <div className="account-settings">
                          <div className="user-profile">
                            <div className="user-avatar">
                              <img src="assets/images/avatar7.png" alt />
                            </div>
                            <h5 className="user-name">Mukesh</h5>
                            <h6 className="user-email">mukesh@gmail.com</h6>
                          </div>
                        </div>
                      </div>
                      <div className="col-xl-9 col-lg-9 col-md-12 col-sm-12 col-12">
                        <div className="row">
                          <div className="col-lg-12">
                            <div className="row gutters">
                              <div className="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                                <h6 className="mb-2 text-primary">Personal Details</h6>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="fullName">First Name</label>
                                  <input type="text" className="form-control" id placeholder="Enter full name" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="fullName">Last Name</label>
                                  <input type="text" className="form-control" id placeholder="Enter full name" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="eMail">Email</label>
                                  <input type="email" className="form-control" id="eMail" placeholder="Enter email ID" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="phone">Phone</label>
                                  <input type="text" className="form-control" id="phone" placeholder="Enter phone number" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="phone">Gender</label>
                                  <select type="text" className="form-control">
                                    <option>Select Gender</option>
                                    <option>Male</option>
                                    <option>Female</option>
                                    <option>Other</option>
                                  </select>
                                </div>
                              </div>
                            </div>
                            <div className="row gutters">
                              <div className="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                                <h6 className="mt-3 mb-2 text-primary">Address</h6>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="Street">Street</label>
                                  <input type="name" className="form-control" id="Street" placeholder="Enter Street" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="ciTy">City</label>
                                  <input type="name" className="form-control" id="ciTy" placeholder="Enter City" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="sTate">State</label>
                                  <input type="text" className="form-control" id="sTate" placeholder="Enter State" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="zIp">Zip Code</label>
                                  <input type="text" className="form-control" id="zIp" placeholder="Zip Code" />
                                </div>
                              </div>
                            </div>
                          </div>
                          <div className="company_details" />
                          <div className="col-lg-12">
                            <div className="row gutters">
                              <div className="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                                <h6 className="mb-2 text-primary">Company Details</h6>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="fullName">Company Name</label>
                                  <input type="text" className="form-control" id placeholder="Enter full name" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="eMail">Pan Number</label>
                                  <input type="email" className="form-control" id placeholder="Enter email ID" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="eMail">Aadhar Number</label>
                                  <input type="email" className="form-control" id placeholder="Enter email ID" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="eMail">GST Number</label>
                                  <input type="email" className="form-control" id placeholder="Enter email ID" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="phone">Phone</label>
                                  <input type="text" className="form-control" id placeholder="Enter phone number" />
                                </div>
                              </div>
                            </div>
                            <div className="row gutters">
                              <div className="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                                <h6 className="mt-3 mb-2 text-primary">Address</h6>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="Street">Street</label>
                                  <input type="name" className="form-control" id placeholder="Enter Street" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="ciTy">City</label>
                                  <input type="name" className="form-control" id placeholder="Enter City" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="sTate">State</label>
                                  <input type="text" className="form-control" id placeholder="Enter State" />
                                </div>
                              </div>
                              <div className="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-12">
                                <div className="form-group">
                                  <label htmlFor="zIp">Zip Code</label>
                                  <input type="text" className="form-control" id placeholder="Zip Code" />
                                </div>
                              </div>
                            </div>
                            <div className="row gutters">
                              <div className="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                                <div className="text-right">
                                  <button type="button" id="submit" name="submit" className="btn btn-secondary">Cancel</button>
                                  <button type="button" id="submit" name="submit" className="btn btn-primary">Update</button>
                                </div>
                              </div>
                            </div>
                          </div> 
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="tab-pane p-3" id="feedback" role="tabpanel">
                  <div className="form-group">
                    <div className="row">
                      <div className="col-lg-2"><label htmlFor="fullName">Name</label></div>
                      <div className="col-lg-4"><input type="text" className="form-control" id placeholder="Name" /></div> 
                    </div></div>
                  <div className="form-group">
                    <div className="row">
                      <div className="col-lg-2"><label htmlFor="fullName">Email ID</label></div>
                      <div className="col-lg-4"><input type="text" className="form-control" id placeholder="Email" /></div> 
                    </div></div>
                  <div className="form-group">
                    <div className="row">
                      <div className="col-lg-2"><label htmlFor="fullName">Message</label></div>
                      <div className="col-lg-4"><textarea type="text" className="form-control" id placeholder defaultValue={""} /></div> 
                    </div>
                  </div>
                  <div className="form-group">
                    <div className="row">
                      <div className="col-lg-2" />
                      <div className="col-lg-6"><a href className="btn btn-success">Submit</a></div>                  
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/*<div class="row">
                          <div class="col-xl-3 col-md-6">
                              <div class="card mini-stat bg-primary">
                                 <a href="">
                                  <div class="card-body mini-stat-img">
                                      <div class="mini-stat-icon">
                                          <i class="mdi mdi-cube-outline float-right"></i>
                                      </div>
                                      <div class="text-white">
                                          <h6 class="text-uppercase mb-3">Account Overview</h6> 
                                      </div>
                                  </div>
                                   </a>
                              </div>
                          </div>
                          <div class="col-xl-3 col-md-6">
                              <div class="card mini-stat bg-primary">
                                 <a href="">
                                  <div class="card-body mini-stat-img">
                                      <div class="mini-stat-icon">
                                          <i class="mdi mdi-buffer float-right"></i>
                                      </div>
                                      <div class="text-white">
                                          <h6 class="text-uppercase mb-3">Orders</h6> 
                                           
                                      </div>
                                  </div>
                                   </a>
                              </div>
                          </div>
                          <div class="col-xl-3 col-md-6">
                              <div class="card mini-stat bg-primary">
                                 <a href="">
                                  <div class="card-body mini-stat-img">
                                      <div class="mini-stat-icon">
                                          <i class="mdi mdi-tag-text-outline float-right"></i>
                                      </div>
                                      <div class="text-white">
                                          <h6 class="text-uppercase mb-3">Adhoc Order</h6> 
                                           
                                      </div>
                                  </div>
                                   </a>
                              </div>
                          </div>
                          <div class="col-xl-3 col-md-6">
                              <div class="card mini-stat bg-primary">
                                 <a href="">
                                  <div class="card-body mini-stat-img">
                                      <div class="mini-stat-icon">
                                          <i class="mdi mdi-briefcase-check float-right"></i>
                                      </div>
                                      <div class="text-white">
                                          <h6 class="text-uppercase mb-3">Documents</h6> 
                                           
                                      </div>
                                  </div>
                                   </a>
                              </div>
                          </div>
                          
                          <div class="col-xl-3 col-md-6">
                              <div class="card mini-stat bg-primary">
                                 <a href="">
                                  <div class="card-body mini-stat-img">
                                      <div class="mini-stat-icon">
                                          <i class="mdi mdi-briefcase-check float-right"></i>
                                      </div>
                                      <div class="text-white">
                                          <h6 class="text-uppercase mb-3">Legal Forms</h6> 
                                           
                                      </div>
                                  </div>
                                   </a>
                              </div>
                          </div>
                     
                          
                          <div class="col-xl-3 col-md-6">
                              <div class="card mini-stat bg-primary">
                                 <a href="">
                                  <div class="card-body mini-stat-img">
                                      <div class="mini-stat-icon">
                                          <i class="mdi mdi-briefcase-check float-right"></i>
                                      </div>
                                      <div class="text-white">
                                          <h6 class="text-uppercase mb-3">Profile Feedback</h6> 
                                           
                                      </div>
                                  </div>
                                  </a>
                              </div>
                          </div>
                          
                          
                          
                      </div>*/}
        {/* <div class="row">
      
                          <div class="col-xl-3">
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 header-title">Monthly Earnings</h4>
      
                                      <div class="row text-center m-t-20">
                                          <div class="col-6">
                                              <h5 class="">$56241</h5>
                                              <p class="text-muted">Marketplace</p>
                                          </div>
                                          <div class="col-6">
                                              <h5 class="">$23651</h5>
                                              <p class="text-muted">Total Income</p>
                                          </div>
                                      </div>
      
                                      <div id="morris-donut-example" class="dashboard-charts morris-charts"></div>
                                  </div>
                              </div>
                          </div>
      
                          <div class="col-xl-6">
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 header-title">Email Sent</h4>
      
                                      <div class="row text-center m-t-20">
                                          <div class="col-4">
                                              <h5 class="">$ 89425</h5>
                                              <p class="text-muted">Marketplace</p>
                                          </div>
                                          <div class="col-4">
                                              <h5 class="">$ 56210</h5>
                                              <p class="text-muted">Total Income</p>
                                          </div>
                                          <div class="col-4">
                                              <h5 class="">$ 8974</h5>
                                              <p class="text-muted">Last Month</p>
                                          </div>
                                      </div>
      
                                      <div id="morris-area-example" class="dashboard-charts morris-charts"></div>
                                  </div>
                              </div>
                          </div>
      
                          <div class="col-xl-3">
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 header-title">Monthly Earnings</h4>
      
                                      <div class="row text-center m-t-20">
                                          <div class="col-6">
                                              <h5 class="">$ 2548</h5>
                                              <p class="text-muted">Marketplace</p>
                                          </div>
                                          <div class="col-6">
                                              <h5 class="">$ 6985</h5>
                                              <p class="text-muted">Total Income</p>
                                          </div>
                                      </div>
      
                                      <div id="morris-bar-stacked" class="dashboard-charts morris-charts"></div>
                                  </div>
                              </div>
                          </div>
      
                      </div>                          
      
                      <div class="row">
                          
                          <div class="col-xl-4 col-lg-6">
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 header-title mb-3">Inbox</h4>
                                      <div class="inbox-wid">
                                          <a href="#" class="text-dark">
                                              <div class="inbox-item">
                                                  <div class="inbox-item-img float-left mr-3"><img src="assets/images/users/user-1.jpg" class="thumb-md rounded-circle" alt=""></div>
                                                  <h6 class="inbox-item-author mt-0 mb-1">Misty</h6>
                                                  <p class="inbox-item-text text-muted mb-0">Hey! there I'm available...</p>
                                                  <p class="inbox-item-date text-muted">13:40 PM</p>
                                              </div>
                                          </a>
                                          <a href="#" class="text-dark">
                                              <div class="inbox-item">
                                                  <div class="inbox-item-img float-left mr-3"><img src="assets/images/users/user-2.jpg" class="thumb-md rounded-circle" alt=""></div>
                                                  <h6 class="inbox-item-author mt-0 mb-1">Melissa</h6>
                                                  <p class="inbox-item-text text-muted mb-0">I've finished it! See you so...</p>
                                                  <p class="inbox-item-date text-muted">13:34 PM</p>
                                              </div>
                                          </a>
                                          <a href="#" class="text-dark">
                                              <div class="inbox-item">
                                                  <div class="inbox-item-img float-left mr-3"><img src="assets/images/users/user-3.jpg" class="thumb-md rounded-circle" alt=""></div>
                                                  <h6 class="inbox-item-author mt-0 mb-1">Dwayne</h6>
                                                  <p class="inbox-item-text text-muted mb-0">This theme is awesome!</p>
                                                  <p class="inbox-item-date text-muted">13:17 PM</p>
                                              </div>
                                          </a>
                                          <a href="#" class="text-dark">
                                              <div class="inbox-item">
                                                  <div class="inbox-item-img float-left mr-3"><img src="assets/images/users/user-4.jpg" class="thumb-md rounded-circle" alt=""></div>
                                                  <h6 class="inbox-item-author mt-0 mb-1">Martin</h6>
                                                  <p class="inbox-item-text text-muted mb-0">Nice to meet you</p>
                                                  <p class="inbox-item-date text-muted">12:20 PM</p>
                                              </div>
                                          </a>
                                          <a href="#" class="text-dark">
                                              <div class="inbox-item">
                                                  <div class="inbox-item-img float-left mr-3"><img src="assets/images/users/user-5.jpg" class="thumb-md rounded-circle" alt=""></div>
                                                  <h6 class="inbox-item-author mt-0 mb-1">Vincent</h6>
                                                  <p class="inbox-item-text text-muted mb-0">Hey! there I'm available...</p>
                                                  <p class="inbox-item-date text-muted">11:47 AM</p>
                                              </div>
                                          </a>
      
                                          <a href="#" class="text-dark">
                                              <div class="inbox-item">
                                                  <div class="inbox-item-img float-left mr-3"><img src="assets/images/users/user-6.jpg" class="thumb-md rounded-circle" alt=""></div>
                                                  <h6 class="inbox-item-author mt-0 mb-1">Robert Chappa</h6>
                                                  <p class="inbox-item-text text-muted mb-0">Hey! there I'm available...</p>
                                                  <p class="inbox-item-date text-muted">10:12 AM</p>
                                              </div>
                                          </a>
                                          
                                      </div>  
                                  </div>
                              </div>
      
                          </div>
                          <div class="col-xl-4 col-lg-6">
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 header-title mb-4">Recent Activity Feed</h4>
      
                                      <ol class="activity-feed mb-0">
                                          <li class="feed-item">
                                              <div class="feed-item-list">
                                                  <span class="date">Jun 25</span>
                                                  <span class="activity-text">Responded to need “Volunteer Activities”</span>
                                              </div>
                                          </li>
                                          <li class="feed-item">
                                              <div class="feed-item-list">
                                                  <span class="date">Jun 24</span>
                                                  <span class="activity-text">Added an interest “Volunteer Activities”</span>
                                              </div>
                                          </li>
                                          <li class="feed-item">
                                              <div class="feed-item-list">
                                                  <span class="date">Jun 23</span>
                                                  <span class="activity-text">Joined the group “Boardsmanship Forum”</span>
                                              </div>
                                          </li>
                                          <li class="feed-item">
                                              <div class="feed-item-list">
                                                  <span class="date">Jun 21</span>
                                                  <span class="activity-text">Responded to need “In-Kind Opportunity”</span>
                                              </div>
                                          </li>
                                      </ol>
      
                                      <div class="text-center">
                                          <a href="#" class="btn btn-sm btn-primary">Load More</a>
                                      </div>
                                  </div>
                              </div>
      
                          </div>
                          <div class="col-xl-4">
                              <div class="card widget-user m-b-20">
                                  <div class="widget-user-desc p-4 text-center bg-primary position-relative">
                                      <i class="fas fa-quote-left h3 text-white-50"></i>
                                      <p class="text-white mb-0">The European languages are members of the same family. Their separate existence is a myth. For science, music, sport, etc, Europe the same vocabulary. The languages only in their grammar.</p>
                                  </div>
                                  <div class="p-4">
                                      <div class="float-left mt-2 mr-3">
                                          <img src="assets/images/users/user-2.jpg" alt="" class="rounded-circle thumb-md">
                                      </div>
                                      <h6 class="mb-1">Marie Minnick</h6>
                                      <p class="text-muted mb-0">Marketing Manager</p>
                                  </div>
                              </div>
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 header-title">Yearly Sales</h4>
                                      <div class="row">
                                          <div class="col-md-4">
                                              <div>
                                                  <h4>52,345</h4>
                                                  <p class="text-muted">The languages only differ grammar</p>
                                                  <a href="#" class="text-primary">Learn more <i class="mdi mdi-chevron-double-right"></i></a>
                                              </div>
                                          </div>
                                          <div class="col-md-8 text-right">
                                              <div id="sparkline"></div>
                                          </div>
                                      </div>
                                  </div>
                              </div>
      
                          </div>
                      </div>
                    
                      <div class="row">
                          <div class="col-xl-6">
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 m-b-30 header-title">Latest Transactions</h4>
      
                                      <div class="table-responsive">
                                          <table class="table table-vertical">
      
                                              <tbody>
                                              <tr>
                                                  <td>
                                                      <img src="assets/images/users/user-2.jpg" alt="user-image" class="thumb-sm rounded-circle mr-2"/>
                                                      Herbert C. Patton
                                                  </td>
                                                  <td><i class="mdi mdi-checkbox-blank-circle text-success"></i> Confirm</td>
                                                  <td>
                                                      $14,584
                                                      <p class="m-0 text-muted font-14">Amount</p>
                                                  </td>
                                                  <td>
                                                      5/12/2016
                                                      <p class="m-0 text-muted font-14">Date</p>
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>
                                                      <img src="assets/images/users/user-3.jpg" alt="user-image" class="thumb-sm rounded-circle mr-2"/>
                                                      Mathias N. Klausen
                                                  </td>
                                                  <td><i class="mdi mdi-checkbox-blank-circle text-warning"></i> Waiting payment</td>
                                                  <td>
                                                      $8,541
                                                      <p class="m-0 text-muted font-14">Amount</p>
                                                  </td>
                                                  <td>
                                                      10/11/2016
                                                      <p class="m-0 text-muted font-14">Date</p>
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>
                                                      <img src="assets/images/users/user-4.jpg" alt="user-image" class="thumb-sm rounded-circle mr-2"/>
                                                      Nikolaj S. Henriksen
                                                  </td>
                                                  <td><i class="mdi mdi-checkbox-blank-circle text-success"></i> Confirm</td>
                                                  <td>
                                                      $954
                                                      <p class="m-0 text-muted font-14">Amount</p>
                                                  </td>
                                                  <td>
                                                      8/11/2016
                                                      <p class="m-0 text-muted font-14">Date</p>
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>
                                                      <img src="assets/images/users/user-5.jpg" alt="user-image" class="thumb-sm rounded-circle mr-2"/>
                                                      Lasse C. Overgaard
                                                  </td>
                                                  <td><i class="mdi mdi-checkbox-blank-circle text-danger"></i> Payment expired</td>
                                                  <td>
                                                      $44,584
                                                      <p class="m-0 text-muted font-14">Amount</p>
                                                  </td>
                                                  <td>
                                                      7/11/2016
                                                      <p class="m-0 text-muted font-14">Date</p>
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>
                                                      <img src="assets/images/users/user-6.jpg" alt="user-image" class="thumb-sm rounded-circle mr-2"/>
                                                      Kasper S. Jessen
                                                  </td>
                                                  <td><i class="mdi mdi-checkbox-blank-circle text-success"></i> Confirm</td>
                                                  <td>
                                                      $8,844
                                                      <p class="m-0 text-muted font-14">Amount</p>
                                                  </td>
                                                  <td>
                                                      1/11/2016
                                                      <p class="m-0 text-muted font-14">Date</p>
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              </tbody>
                                          </table>
                                      </div>
                                  </div>
                              </div>
                          </div>
      
                          <div class="col-xl-6">
                              <div class="card m-b-20">
                                  <div class="card-body">
                                      <h4 class="mt-0 m-b-30 header-title">Latest Orders</h4>
      
                                      <div class="table-responsive">
                                          <table class="table table-vertical mb-1">
      
                                              <tbody>
                                              <tr>
                                                  <td>#12354781</td>
                                                  <td>
                                                      <img src="assets/images/users/user-1.jpg" alt="user-image" class="thumb-sm mr-2 rounded-circle"/>
                                                      Riverston Glass Chair
                                                  </td>
                                                  <td><span class="badge badge-pill badge-success">Delivered</span></td>
                                                  <td>
                                                      $185
                                                  </td>
                                                  <td>
                                                      5/12/2016
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>#52140300</td>
                                                  <td>
                                                      <img src="assets/images/users/user-2.jpg" alt="user-image" class="thumb-sm mr-2 rounded-circle"/>
                                                      Shine Company Catalina
                                                  </td>
                                                  <td><span class="badge badge-pill badge-success">Delivered</span></td>
                                                  <td>
                                                      $1,024
                                                  </td>
                                                  <td>
                                                      5/12/2016
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>#96254137</td>
                                                  <td>
                                                      <img src="assets/images/users/user-3.jpg" alt="user-image" class="thumb-sm mr-2 rounded-circle"/>
                                                      Trex Outdoor Furniture Cape
                                                  </td>
                                                  <td><span class="badge badge-pill badge-danger">Cancel</span></td>
                                                  <td>
                                                      $657
                                                  </td>
                                                  <td>
                                                      5/12/2016
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>#12365474</td>
                                                  <td>
                                                      <img src="assets/images/users/user-4.jpg" alt="user-image" class="thumb-sm mr-2 rounded-circle"/>
                                                      Oasis Bathroom Teak Corner
                                                  </td>
                                                  <td><span class="badge badge-pill badge-warning">Shipped</span></td>
                                                  <td>
                                                      $8451
                                                  </td>
                                                  <td>
                                                      5/12/2016
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              <tr>
                                                  <td>#85214796</td>
                                                  <td>
                                                      <img src="assets/images/users/user-5.jpg" alt="user-image" class="thumb-sm mr-2 rounded-circle"/>
                                                      BeoPlay Speaker
                                                  </td>
                                                  <td><span class="badge badge-pill badge-success">Delivered</span></td>
                                                  <td>
                                                      $584
                                                  </td>
                                                  <td>
                                                      5/12/2016
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
                                              <tr>
                                                  <td>#12354781</td>
                                                  <td>
                                                      <img src="assets/images/users/user-6.jpg" alt="user-image" class="thumb-sm mr-2 rounded-circle"/>
                                                      Riverston Glass Chair
                                                  </td>
                                                  <td><span class="badge badge-pill badge-success">Delivered</span></td>
                                                  <td>
                                                      $185
                                                  </td>
                                                  <td>
                                                      5/12/2016
                                                  </td>
                                                  <td>
                                                      <button type="button" class="btn btn-secondary btn-sm waves-effect waves-light">Edit</button>
                                                  </td>
                                              </tr>
      
                                              </tbody>
                                          </table>
                                      </div>
                                  </div>
                              </div>
                          </div>
                      </div>*/}
      </div> 
    </div>  
    <footer className="footer">
      © 2022 - 2023   <span className="d-none d-sm-inline-block"> <i className="mdi mdi-heart text-danger" /> by Bol 7</span>.
    </footer>
  </div>
</div>
